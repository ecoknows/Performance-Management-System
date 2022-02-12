
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
from django.db.models import Q

from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.admin.edit_handlers import (
    FieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from performance_management_system import IntegerResource, StringResource
from performance_management_system.users.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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

        return self.render(
            request,
            context_overrides={
                'user_model' : request.user.client,
                'notification_url': self.url,
                'reports_index': ReportsClient.objects.live().first(),
            },
            template="base/notifications.html",
        )

    @route(r'^notifications/search/$')
    def notifications_search(self, request):
        from performance_management_system.hr.models import Notification

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        message = request.GET.get('message', '')
        time = request.GET.get('time', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        notifications = None

        if name or message or time or status or position or sort:

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
    
    @route(r'^notifications/(\d+)/$')
    def notification_view(self, request, notification_id):
        from performance_management_system.hr.models import EvaluationCategories, EvaluationPage, EvaluationRateAssign
        from performance_management_system.base.models import Notification

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
                'user_model' : request.user.client,
                'notification_url': self.url,
                'notification': notification,
                'categories' : categories,
                'category_percentages': category_percentages,
                'reports_index': ReportsClient.objects.live().first(),
            },
            template="base/notifications_view.html",
        )

    @route(r'^notifications/(\d+)/evaluation/$')
    def notification_evaluation(self, request, notification_id):
        from performance_management_system.base.models import Notification, EvaluationPage, EvaluationCategories, EvaluationRateAssign, EvaluationTask, EvaluationRates

        notification = Notification.objects.get(pk=notification_id)
        user_evaluation = notification.user_evaluation
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation

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
                        evaluation_rate_assign.rate= question_rate
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

        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'user_model' : request.user.client,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'notifications',
                'notification_url': self.url,
                'submit_success': submit_success,
                'reports_index': ReportsClient.objects.live().first(),
            },
            template="base/evaluation_page.html",
        )
    
    class Meta:
        abstract = True
        
class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    profile_pic = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    company = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    contact_number = models.CharField(max_length=255, null=True)

    panels = [
        ImageChooserPanel('profile_pic'),
        FieldPanel('company'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
    ]
    
    @property
    def client_id(self):
        return self.user.username;
    
    @property
    def display_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.profile_pic.get_rendition('fill-200x100').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''

    def __str__(self):
        return self.company
    
    def delete(self):
        if self.user:
            self.user.delete()
        super().delete()        

class ReportsClient(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ['ClientIndexPage']

    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 7)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^$') 
    def default_route(self, request):
        
        return self.render(
            request,
            context_overrides={
                'user_model': request.user.client,
                'notification_url' : ClientIndexPage.objects.live().first().url ,
                'reports_index': self,
            })

    @route(r'^(\d+)/$')
    def details_user_route(self, request, user_evaluation_id):
        from performance_management_system.base.models import EvaluationCategories, EvaluationPage, UserEvaluation, EvaluationRateAssign
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        employee = user_evaluation.employee
        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []
        overall_performance = 0


        for category in categories:
            rate_assigns = EvaluationRateAssign.objects.filter(
                evaluation_rate__evaluation_categories=category,
                user_evaluation = user_evaluation
            )
            percentage = 0
            for rate_assign in rate_assigns:
                percentage = rate_assign.rate + percentage

            rate_assign_len = len(rate_assigns) 

            if rate_assign_len:
                percentage = (percentage / (rate_assign_len * max_rate))
            else:
                percentage = 0
            
            overall_performance = overall_performance + percentage
            
            category_percentages.append([category,percentage])

        if overall_performance != 0:
            overall_performance = overall_performance / len(categories)
        
        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'user_model': request.user.client ,
            'category_percentages': category_percentages,
            'current_menu':'reports',
            'notification_url': ClientIndexPage.objects.live().first().url,
            'reports_index': self,
            'max_rate' : max_rate,
            'overall_performance': overall_performance,
            'employee': employee,
            },
            template='hr/employee_details_page.html'
            
        )

    @route(r'^(\d+)/evaluation/$')
    def client_evaluation_details(self, request, user_evaluation_id):
        from performance_management_system.base.models import UserEvaluation, EvaluationPage, EvaluationCategories
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation

        
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'user_model' : request.user.client,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'reports',
                'notification_url': ClientIndexPage.objects.live().first().url,
                'reports_index': self,
            },
            template="base/evaluation_page.html",
        )

    @route(r'^search/evaluations/$')
    def evaluation_search(self, request):

        from performance_management_system.base.models import UserEvaluation

        page = request.GET.get('page', 1)

        employee = request.GET.get('employee', '')
        project_assign = request.GET.get('project_assign', '')
        performance = request.GET.get('performance', '')
        date = request.GET.get('date', '')

        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        user_evaluations = None

        if employee or project_assign or date or performance or sort:

            if employee:
                employee_name = employee.split()
                qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) for query in employee_name])
                
                user_evaluations = UserEvaluation.objects.filter(qset1).distinct()

                if sort:
                    user_evaluations = user_evaluations.filter(project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date).order_by(sort)
                else:
                    user_evaluations = user_evaluations.filter(project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date)
            else:
                if sort:
                    user_evaluations = UserEvaluation.objects.filter(project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date).order_by(sort)
                else:
                    user_evaluations = UserEvaluation.objects.filter(project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date)
            
        else:
            if sort:
                user_evaluations = UserEvaluation.objects.all().order_by(sort)
            else:
                user_evaluations = UserEvaluation.objects.all().order_by('-submit_date','assigned_date')
        

        user_evaluations = self.paginate_data(user_evaluations.filter(client=request.user.client), page)
        max_pages = user_evaluations.paginator.num_pages
        starting_point = user_evaluations.number
        next_number = 1
        previous_number = 1

        if user_evaluations.has_next():
            next_number = user_evaluations.next_page_number()
        
        if user_evaluations.has_previous():
            previous_number = user_evaluations.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 

        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'client/search_reports.html',
                        {
                            'user_evaluations' : user_evaluations,
                            'timezone': timezone,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': user_evaluations,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': user_evaluations.number,
                },
            )

class ClientIndexPage(BaseAbstractPage):
    max_count = 1
    parent_page_types = ['base.BaseIndexPage']
    
    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 8)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^$') 
    def default_route(self, request):
        from performance_management_system.base.models import EvaluationPage
        notification_url = self.url
        
        return self.render(
            request,
            context_overrides={
                'user_model': request.user.client,
                'current_menu': 'dashboard',
                'title': 'EMPLOYEES',
                'evaluation_index': EvaluationPage.objects.live().first().url,
                'notification_url': notification_url,
                'reports_index': ReportsClient.objects.live().first(),
            }
        )
    
    @route(r'^search/employees/$')
    def employee_search(self, request):
        from performance_management_system.base.models import UserEvaluation, EvaluationPage

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        user_evaluations = None

        if name or address or contact_number or status or sort or position:

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) for query in name])
                user_evaluations = UserEvaluation.objects.filter(qset1, client=request.user.client).distinct()
                if sort:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position).order_by(sort)
                else:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position)
            else:
                if sort:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position, client=request.user.client).order_by(sort)
                else:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position, client=request.user.client)
            
            if status == 'for-evaluation':
                user_evaluations = user_evaluations.filter( submit_date__isnull=True)
            if status == 'done-evaluating':
                user_evaluations = user_evaluations.filter( submit_date__isnull=False)
            
        else:
            if sort:
                user_evaluations = UserEvaluation.objects.filter(client=request.user.client).order_by(sort)
            else:
                user_evaluations = UserEvaluation.objects.filter(client=request.user.client).order_by('-submit_date', 'assigned_date')

        user_evaluations = self.paginate_data(user_evaluations, page)
        max_pages = user_evaluations.paginator.num_pages
        starting_point = user_evaluations.number
        next_number = 1
        previous_number = 1

        if user_evaluations.has_next():
            next_number = user_evaluations.next_page_number()
        
        if user_evaluations.has_previous():
            previous_number = user_evaluations.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 


        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'client/search_employee_specified.html',
                        {
                            'user_evaluations' : user_evaluations,
                            'evaluation_page_index': EvaluationPage.objects.live().first(),
                            'timezone': timezone,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': user_evaluations,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': user_evaluations.number,
                },
            )
        
    @route(r'^(\d+)/resign/$')
    def resign_employee(self,request, id):
        from performance_management_system.base.models import UserEvaluation
        
        user_eval = UserEvaluation.objects.get(id=id)
        user_eval.delete()
        return HttpResponseRedirect('../../')