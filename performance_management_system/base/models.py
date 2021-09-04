

from django.template.response import TemplateResponse
from django.dispatch.dispatcher import receiver
from django.http import HttpResponseRedirect
from django.db import models
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.http import JsonResponse
from django.template.loader import render_to_string
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    RichTextField
)

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from performance_management_system.users.models import User
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client, ClientIndexPage, ReportsClient
from performance_management_system import CALENDAR, NOTIFICATION_TYPE
from django.contrib.postgres.fields import ArrayField
from itertools import chain
import operator
from functools import reduce

class BaseAbstractPage(RoutablePageMixin, Page):

    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 8)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^notifications/$')
    def notification(self, request):
        from performance_management_system.hr.models import EmployeeListPage, AssignEmployee, ClientListPage

        return self.render(
            request,
            context_overrides={
                'user_model' : request.user.hradmin,
                'notification_url': self.url,
                'client_list_index':  ClientListPage.objects.live().first(),
                'employee_list_index': EmployeeListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
            },
            template="base/notifications.html",
        )

    @route(r'^notifications/(\d+)/$')
    def notification_view(self, request, notification_id):
        from performance_management_system.hr.models import EmployeeListPage, AssignEmployee, ClientListPage, EmployeeDetailsPage
        notification = Notification.objects.get(pk=notification_id)

        if notification.seen == False:
            notification.seen = True
            notification.save()

        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []
        selected_user_evaluation = notification.user_evaluation
        for category in categories:
            rate_assigns = EvaluationRateAssign.objects.filter(
                evaluation_rate__evaluation_categories=category,
                user_evaluation = selected_user_evaluation
            )
            percentage = 0
            for rate_assign in rate_assigns:
                percentage = rate_assign.rate + percentage

            rate_assign_len = len(rate_assigns) 

            if rate_assign_len:
                percentage = (percentage / (rate_assign_len * max_rate)) * 100
            else:
                percentage = 0
            
            category_percentages.append(percentage)

        return self.render(
            request,
            context_overrides={
                'user_model' : request.user.hradmin,
                'notification_url': self.url,
                'notification': notification,
                'client_list_index':  ClientListPage.objects.live().first(),
                'employee_list_index': EmployeeListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'categories' : categories,
                'category_percentages': category_percentages,
            },
            template="base/notifications_view.html",
        )

    @route(r'^notifications/search/$')
    def notifications_search(self, request):

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        message = request.GET.get('message', '')
        time = request.GET.get('time', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        notifications = None

        if name or message or time or status or position:

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(user_evaluation__employee__first_name__icontains=query) | Q(user_evaluation__employee__last_name__icontains=query) for query in name])
                notifications = Notification.objects.filter(qset1, reciever=request.user).distinct()
                if sort:
                    notifications = notifications.filter( message__icontains=message, created_at__icontains=time, seen__icontains=status).order_by(sort)
                else:
                    notifications = notifications.filter( message__icontains=message, created_at__icontains=time, seen__icontains=status)
            else:
                if sort:
                    notifications = Notification.objects.filter( message__icontains=message, created_at__icontains=time, seen__icontains=status, reciever=request.user).order_by(sort)
                else:
                    notifications = Notification.objects.filter( message__icontains=message, created_at__icontains=time, seen__icontains=status, reciever=request.user)
            
        else:
            if sort:
                notifications = Notification.objects.filter(reciever=request.user).order_by(sort)
            else:
                notifications = Notification.objects.filter(reciever=request.user).order_by('seen','-created_at')


        notifications = self.paginate_data(notifications, page)
        max_pages = notifications.paginator.num_pages
        starting_point = notifications.number
        next_number = 1
        previous_number = 1

        if notifications.has_next():
            next_number = notifications.next_page_number()
        
        if notifications.has_previous():
            previous_number = notifications.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 



        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'base/search_notifications.html',
                        {
                            'notifications' : notifications,
                            'is_hr': request.user.is_hr,
                            'timezone': timezone,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': notifications,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': notifications.number,
                },
            )
    
    @route(r'^notifications/(\d+)/evaluation/$')
    def notification_evaluation(self, request, notification_id):
        
        notification = Notification.objects.get(pk=notification_id)
        user_evaluation = notification.user_evaluation
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation

        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'notifications',
                'notification_url': self.url,
            },
            template="base/evaluation_page.html",
        )
    
    class Meta:
        abstract = True

class BaseIndexPage(Page):
    max_count = 1
    def serve(self, request):
        if request.user.is_superuser == True:
            return HttpResponseRedirect('/admin/')
        elif request.user.is_authenticated == False:
            return HttpResponseRedirect('/login/')
        elif request.user.is_hr:
            from performance_management_system.hr.models import HRIndexPage
            hr_index_page = HRIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(hr_index_page[0].slug)
        elif request.user.is_employee:
            from performance_management_system.employee.models import EmployeeIndexPage
            employee_index_page = EmployeeIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(employee_index_page[0].slug)
        elif request.user.is_client:
            from performance_management_system.client.models import ClientIndexPage
            client_index_page = ClientIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(client_index_page[0].slug)
        
        return HttpResponseRedirect('/logout/')

class EvaluationRates(ClusterableModel):
    evaluation_categories = ParentalKey('EvaluationCategories', on_delete=models.CASCADE, related_name='evaluation_rates')
    
    name = models.TextField(
        max_length=255,
        null=True,   
        verbose_name='Question'
    )
    
    panels = [
        FieldPanel('name'),
    ]
    
    def __str__(self):
        return self.name
    
class EvaluationCategories(ClusterableModel):
    
    evaluation_page = ParentalKey(
        'EvaluationPage', 
        null=True,
        on_delete=models.CASCADE, 
        related_name='evaluation_categories'
    )
    
    
    category_name = models.TextField(
        max_length=255,
        null=True,
        verbose_name='Category'
    )
    
    @property
    def list_rates(self):
        return self.evaluation_rates.all()
    
    def __str__(self):
        return self.category_name
     
    panels = [
        FieldPanel('category_name'),
        InlinePanel('evaluation_rates', label="Evaluation Rates"),
    ]

class EvaluationTask(models.Model):
    category = models.ForeignKey(
        EvaluationCategories,
        null=True,
        on_delete=models.CASCADE,
    )

    user_evaluation = models.ForeignKey(
        'UserEvaluation',
        null=True,
        on_delete=models.CASCADE,
        related_name='evaluation_task',
    )

    text = models.CharField(
        max_length=255,
        null=True
    )

class EvaluationRateAssign(Orderable):
    
    user_evaluation = ParentalKey(
        'UserEvaluation', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='evaluation_rates_assign')
    
    evaluation_rate = ParentalKey(
        'EvaluationRates', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='evaluation_rates_assign')
    
    
    rate = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('evaluation_rates'),
    ]
    
class UserEvaluation(ClusterableModel, models.Model):
    employee = models.ForeignKey(
        Employee,
        null=True,
        related_name='user_evaluation',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client,
        null=True,
        related_name='user_evaluation',
        on_delete=models.CASCADE
    )
    
    submit_date = models.DateTimeField(null=True)
    assigned_date = models.DateTimeField( null=True)
    searchable_assigned_date = models.CharField(max_length=255, null=True)
    project_assign = models.CharField(max_length=255, null=True)
    late_and_absence = ArrayField(ArrayField(models.IntegerField()), null=True)

    performance = models.DecimalField(
        max_digits=5,
        decimal_places=2, 
        default=0.0
    )

    hr_admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    
    panels = [
        FieldPanel('employee'),
        FieldPanel('client'),
        FieldPanel('assigned_date'),
        FieldPanel('searchable_assigned_date'),
    ]

    def __str__(self):
        return self.employee.last_name + ' to ' + self.client.company
            
class EvaluationPage(RoutablePageMixin, Page):
    max_count = 1
    evaluation_max_rate = models.IntegerField(default=0)
    legend_evaluation = RichTextField(null=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('evaluation_max_rate'),
        FieldPanel('legend_evaluation')
    ]

    categories_panels = [
        InlinePanel('evaluation_categories', label="Evaluation Categories"),
    ]
    
    parent_page_types = ['client.ClientIndexPage']

    edit_handler  = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(categories_panels, heading="Categories"),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading='Settings Stuff'),
        ]
    )


    def get_context(self, request):
        context = super().get_context(request)
        if request.user.client == None: 
            return context
        for user_evaluation in  request.user.client.user_evaluation.all():
            context['user_evaluation'] = user_evaluation
        context['evaluation_categories'] = EvaluationCategories.objects.all()
            
        return context

    @route(r'^$') 
    def default_route(self, request):
        return HttpResponseRedirect('../')
    
    def get_menu_list(self):
        
        return [
            [ClientIndexPage.objects.live().first().url,'Employees']
        ]
    
    @route(r'^(\d+)/$', name='id')
    def evaluate_user_with_id(self, request, id):
        user_evaluation = UserEvaluation.objects.get(pk=id)
        submit_success = None
        performance = 0
        rates_length = 0

        if request.method == 'POST' and request.POST.get('submit-btn', None):
            
            for category in EvaluationCategories.objects.all():
                for rate in category.evaluation_rates.all():
                    evaluation_rate_assign, created = EvaluationRateAssign.objects.get_or_create(
                        user_evaluation=user_evaluation,
                        evaluation_rate=rate,
                    )

                    if evaluation_rate_assign:
                        question_rate = int(request.POST['question-'+str(rate.pk)] )
                        evaluation_rate_assign.rate = question_rate
                        evaluation_rate_assign.save()
                        performance = question_rate + performance

                    rates_length = rates_length + 1

                task = request.POST['task-'+str(category.pk)]

                EvaluationTask.objects.create(
                    category=category,
                    user_evaluation=user_evaluation,
                    text=task
                )
                        
            # update_user_evaluation = UserEvaluation.objects.get(pk=id)
            late_and_absences = []
            for count in range(12):
                late = request.POST['late-'+str(count)]
                absence = request.POST['absence-'+str(count)]

                late_and_absences.append([late,absence])
            

            user_evaluation.submit_date = timezone.now()
            user_evaluation.late_and_absence = late_and_absences 
            user_evaluation.performance = performance / rates_length
            user_evaluation.save()

            Notification.objects.create(
                reciever=user_evaluation.hr_admin,
                message=user_evaluation.client.company+' has already evaluated',
                user_evaluation=user_evaluation,
                notification_type='client-evaluated-hr',
            )
            
            Notification.objects.create(
                reciever=user_evaluation.employee.user,
                message=user_evaluation.client.company+' has already evaluated',
                user_evaluation=user_evaluation,
                notification_type='client-evaluated-employee',
            )
            

            Notification.objects.create(
                reciever=user_evaluation.client.user,
                message='Thank you for evaluating, I have send the result to ' + str(user_evaluation.employee),
                user_evaluation=user_evaluation,
                hr_admin=user_evaluation.hr_admin.hradmin,
                notification_type='evaluated-form-is-send-to-employee',
            )
            
            submit_success = 'success'


        menu_lists = self.get_menu_list()
        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'menu_lists': menu_lists,
            'notification_url':ClientIndexPage.objects.live().first().url,
            'user_model': request.user.client,
            'employee_model': user_evaluation.employee,
            'submit_success': submit_success,
            'reports_index': ReportsClient.objects.live().first(),
            'current_menu' : 'dashboard'
            }
        )

class Notification(models.Model):
    reciever = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='notifications'
    )

    message = models.CharField(
        max_length=255,
        null=True,
    )

    seen = models.BooleanField(default=False)

    user_evaluation = models.ForeignKey(
        UserEvaluation,
        on_delete=models.CASCADE,
        null=True,
    )

    hr_admin = models.ForeignKey(
        'hr.HrAdmin',
        on_delete=models.CASCADE,
        null=True,
    )

    notification_type = models.CharField(
        max_length=255,
        choices=NOTIFICATION_TYPE,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)

class CalendarOrderable(Orderable):
    page = ParentalKey("RulesSettings", related_name="calendar_orderable")

    count = models.IntegerField(default=0)

    calendar = models.CharField(
        max_length=255,
        choices=CALENDAR,
    )

@register_setting(icon='date')
class RulesSettings(BaseSetting, ClusterableModel):

    limit_message = models.CharField(
        max_length=255,
        null=True,
    )

    panels = [
        FieldPanel(
            'limit_message'
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "calendar_orderable",
                    max_num=5, 
                    min_num=1, 
                    label="Rule"
                )
            ],
            heading="Rules",
        ),
    ]

    class Meta:
        verbose_name = 'Rules'