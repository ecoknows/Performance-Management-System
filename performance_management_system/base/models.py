

from performance_management_system import NOTIFICATION_TYPE
from django.dispatch.dispatcher import receiver
from django.http import HttpResponseRedirect
from django.db import models
from django.utils import timezone

from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.http import JsonResponse
from django.template.loader import render_to_string

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
    RichTextField
)

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from performance_management_system.users.models import User
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client, ClientIndexPage

class BaseAbstractPage(RoutablePageMixin, Page):
    
    @route(r'^notifications/$')
    def notification(self, request):
        from performance_management_system.hr.models import HRIndexPage

        user_model = None
        if request.user.is_employee:
            user_model = request.user.employee
        if request.user.is_client:
            user_model = request.user.client
        if request.user.is_hr:
            user_model = request.user.hradmin
        
        notifications = Notification.objects.filter(reciever=request.user).order_by('-created_at')

        notification_id = request.GET.get('notification_id', None)
        make_it_seen = request.GET.get('make_it_seen', False)

        if notification_id:
            from performance_management_system.hr.models import EmployeeDetailsPage
            notification = Notification.objects.get(pk=notification_id)
            if make_it_seen: 
                notification.seen = True
                notification.save()
            
            selected_user_evaluation = notification.user_evaluation

            categories = EvaluationCategories.objects.all()
            max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
            category_percentages = []
            for category in categories:
                rate_assigns = EvaluationRateAssign.objects.filter(
                    evaluation_rate__evaluation_categories=category,
                    user_evaluation = selected_user_evaluation
                )
                percentage = 0
                for rate_assign in rate_assigns:
                    percentage = rate_assign.rate + percentage
                percentage = (percentage / (len(rate_assigns) * max_rate)) * 100
                category_percentages.append(percentage)
                




            return JsonResponse(
                data={
                    'selected_html' : render_to_string(
                        'base/selected_notification.html', 
                        {
                            'notification' : notification,
                            'categories': categories,
                            'category_percentages': category_percentages,
                            'evaluation_index_page': EmployeeDetailsPage.objects.live().first().url + str(selected_user_evaluation.employee.pk) +'/clients/' + str(selected_user_evaluation.pk)
                        }
                    ),
                    'notification_html' :  render_to_string(
                        'hr/counter_notification.html',
                        {
                            'notifications_count' : 4,
                            'id': request.user.id
                        }
                    )
                },
               
            )

        return self.render(
            request,
            context_overrides={
                'user_model' : user_model,
                'notifications' : notifications,
                'notification_url': self.url,
                'search_page': HRIndexPage.objects.live().first(),
                'notifications_count' : len(notifications),
            },
            template="base/notifications.html",
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

# ABSTRACT
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
    
# ABSTRACT
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
    
    percentage = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    submit_date = models.DateTimeField(null=True)
    assigned_date = models.DateTimeField(auto_now_add=True, null=True)
    project_assign = models.CharField(max_length=255, null=True)

    hr_admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    
    panels = [
        FieldPanel('employee'),
        FieldPanel('client'),
    ]
            

class EvaluationPage(RoutablePageMixin, Page):
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
        evaluation_sum = 0
        submit_success = None

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
                        evaluation_sum = evaluation_sum + question_rate
                        evaluation_rate_assign.save()
                        
            update_user_evaluation = UserEvaluation.objects.get(pk=id)

            perfect_rate = len(EvaluationRates.objects.all()) * self.evaluation_max_rate
            update_user_evaluation.percentage = (evaluation_sum / perfect_rate) * 100
            update_user_evaluation.submit_date = timezone.now()
            update_user_evaluation.save()

            employee = user_evaluation.employee
            employee_not_evaluated = employee.user_evaluation.filter(percentage=0)

            if len(employee_not_evaluated) == 0:
                employee.status = 'evaluated'
                employee.save()

            client = user_evaluation.client
            client_not_evaluated = client.user_evaluation.filter(percentage=0)
            
            if len(client_not_evaluated) == 0:
                client.status = 'evaluated'
                client.save()

            Notification.objects.create(
                reciever=update_user_evaluation.hr_admin,
                message=update_user_evaluation.client.company+' has already evaluated',
                user_evaluation=update_user_evaluation,
                notification_type='client-evaluated-hr',
            )
            
            Notification.objects.create(
                reciever=update_user_evaluation.employee.user,
                message=update_user_evaluation.client.company+' has already evaluated',
                user_evaluation=update_user_evaluation,
                notification_type='client-evaluated-employee',
            )
            

            Notification.objects.create(
                reciever=update_user_evaluation.client.user,
                message='Thank you for evaluating, I have send the result to ' + str(update_user_evaluation.employee),
                user_evaluation=update_user_evaluation,
                hr_admin=update_user_evaluation.hr_admin.hradmin,
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
            'search_page': ClientIndexPage.objects.live().first()
            }
        )

class Notification(models.Model):
    reciever = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
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
