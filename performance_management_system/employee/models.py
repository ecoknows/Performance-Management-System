
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.db.models import Q

from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from performance_management_system import IntegerResource, StringResource, IS_EVALUATED
from performance_management_system.users.models import User
from performance_management_system.client.models import Client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import operator
from functools import reduce


class BaseAbstractPage(RoutablePageMixin, Page):

    def paginate_notification(self, notifications, current_page, max_page):
        paginator = Paginator(notifications, max_page)

        try:
            notifications = paginator.page(current_page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        
        return notifications
    
    @route(r'^notifications/$')
    def notification(self, request):
        from performance_management_system.base.models import Notification, EvaluationCategories,EvaluationPage,EvaluationRateAssign
        
        current_page = request.GET.get('current_page', None)


        if current_page:
            notifications = Notification.objects.filter(reciever=request.user).order_by('-created_at')
            starting_point = len(notifications)

            if starting_point >= 10:
                notifications = notifications[10:]
            else:
                notifications = notifications[starting_point:]

            notifications =  self.paginate_notification(notifications, current_page, 3)

            has_next = notifications.has_next()
            next_number = None
            if has_next:
                next_number = notifications.next_page_number()

            return JsonResponse(
                data={
                    'next_number': next_number,
                    'has_next': has_next,
                    'html': render_to_string('base/paginated_notification.html',{'notifications' : notifications}) 
                }
            )
        

        hr_admin_id = request.GET.get('hr_admin_id', None)
        notification_id = request.GET.get('notification_id', None)
        make_it_seen = request.GET.get('make_it_seen', False)


        if hr_admin_id:
            from performance_management_system.hr.models import HrAdmin
            notification = Notification.objects.get(pk=notification_id)

            if make_it_seen: 
                notification.seen = True
                notification.save()


            selected_hr_admin = HrAdmin.objects.get(pk = hr_admin_id)
            on_evaluation_employee = None

            if notification.notification_type == 'notify-evaluated-all-client':
                on_evaluation_employee = request.user.employee.user_evaluation.filter(percentage=0)
            elif notification.notification_type == 'notify-evaluated-specific-client' or notification.notification_type == 'new-client-employee' or notification.notification_type == 'client-has-been-notify' :
                on_evaluation_employee = notification.user_evaluation

            return JsonResponse(
                data={
                    'selected_html' : render_to_string(
                        'base/selected_notification.html', 
                        {
                            'notification': notification,
                            'selected_hr_admin': selected_hr_admin,
                            'on_evaluation_employee': on_evaluation_employee,
                            'evaluation_index_page': EmployeeIndexPage.objects.live().first().url
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
                rate_assign_len = len(rate_assigns) 
                
                if rate_assign_len:
                    percentage = (percentage / (rate_assign_len * max_rate)) * 100
                else:
                    percentage = 0
                category_percentages.append(percentage)

            
                

            return JsonResponse(
                data={
                    'selected_html' : render_to_string(
                        'base/selected_notification.html', 
                        {
                            'notification' : notification,
                            'categories': categories,
                            'category_percentages': category_percentages,
                            'evaluation_index_page': EmployeeIndexPage.objects.live().first().url
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
        
        notifications = Notification.objects.filter(reciever=request.user).order_by('-created_at')

        return self.render(
            request,
            context_overrides={
                'user_model' : request.user.employee,
                'notifications' : self.paginate_notification(notifications, current_page, 10),
                'notification_url': self.url,
                'menu_lists': [
                    [EmployeeIndexPage.objects.live().first().url,'Dashboard'],
                    [EmployeeIndexPage.objects.live().first().url+ 'client','Client'],
                ],
                'notifications_count' : len(notifications),
                'search_page': EmployeeIndexPage.objects.live().first()
            },
            template="base/notifications.html",
        )

    
    class Meta:
        abstract = True

class Employee(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE,
    )

    profile_pic = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    first_name = models.CharField(max_length=25, null=True)
    middle_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=25,null=True)
    address = models.CharField(max_length=255, null=True)
    contact_number = models.CharField(max_length=255, null=True)
    birth_day = models.DateField()
    position = models.CharField(max_length=255, null=True)

    status = models.CharField(
        max_length=255,
        choices=IS_EVALUATED,
        default='none'
    )
    

    panels = [
        ImageChooserPanel('profile_pic'),
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('middle_name'),
            FieldPanel('last_name'),    
        ], heading='Employee Complete Name'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
        FieldPanel('birth_day'),
        FieldPanel('position'),
    ]
    
    @property
    def employee_id(self):
        return self.user.username
    
    @property
    def employee(self):
        return self.last_name + ', ' + self.first_name + ' ' + self.middle_name[0] + '.'
        
    
    @property
    def display_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.profile_pic.get_rendition('fill-50x50').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''

    def __str__(self):
        return self.employee

    def delete(self):
        if self.user:
            self.user.delete()
        super().delete()
            
    
class EmployeeIndexPage(BaseAbstractPage):
    max_count = 1
    filter = None
    parent_page_types = ['base.BaseIndexPage']

    @route(r'^search/$')
    def pop_search(self, request):
        from performance_management_system.base.models import UserEvaluation

        search_query = request.GET.get('search_query', None).split()

        if search_query :        
            qset2 =  reduce(operator.__or__, [Q(client__company__icontains=query) for query in search_query])

            user_evaluations = UserEvaluation.objects.filter(qset2, employee=request.user.employee).distinct()

            if len(user_evaluations) == 0:
                return JsonResponse(data={
                    'empty': True
                })

            return TemplateResponse(request, 'employee/pop_search.html', {
                'results' : user_evaluations,
                'user_evaluation_details_index' : self,
            })
        return JsonResponse(data={
            'empty': True
        })

    def get_menu_list(self):
        return [
                  ['client', 'Client'],
               ]


    @route(r'^$')
    def dash_board(self, request):
        from performance_management_system.base.models import EvaluationCategories, UserEvaluation, EvaluationRateAssign, EvaluationPage
        user_evaluation = UserEvaluation.objects.filter(employee=request.user.employee).first()
        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []

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
            
            category_percentages.append([category,percentage])
        

        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'user_model': request.user.employee ,
            'category_percentages': category_percentages,
            'current_menu':'dashboard'
            },
            template='hr/employee_details_page.html'
        )
    
    @route(r'^client/$')
    def current_client(self, request):
        from performance_management_system.base.models import UserEvaluation, EvaluationCategories, EvaluationPage, EvaluationRateAssign
        
        filter_query = request.GET.get('filter', None)
        filter_text = None
        
        if filter_query:
            if filter_query == 'on-evaluation':
                filter_text = 'On Evaluation'
            elif filter_query  == 'evaluated':
                filter_text = 'Evaluated'


        menu_lists = [
            (self.url,'Dashboard'),
            [self.url +'client', 'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]

        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []

        try:
            latest_evaluation = UserEvaluation.objects.filter(employee=request.user.employee).latest('assigned_date')

            for category in categories:
                rate_assigns = EvaluationRateAssign.objects.filter(
                    evaluation_rate__evaluation_categories=category,
                    user_evaluation = latest_evaluation
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
        except UserEvaluation.DoesNotExist:
            latest_evaluation = None
                


        return self.render(
            request,
            context_overrides={
                'filter': self.filter,
                'menu_lists': menu_lists,
                'notification_url' : self.url,
                'latest_evaluation': latest_evaluation,
                'search_page' : self,
                'filter_query': filter_query,
                'filter_text': filter_text,
                'categories': categories,
                'category_percentages': category_percentages,
            },
            template='employee/client_list.html'
        )
    
    @route(r'evaluation/(\d+)/$')
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
                'disabled' : True,
                'user_model' : request.user.employee,
                'employee_model': user_evaluation.client,
                'notification_url' : self.url,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'search_page' : self,
                'current_menu':'dashboard'
            },
            template="base/evaluation_page.html",
        )

    @route(r'^search/client/$')
    def client_search_specified(self, request):
        from performance_management_system.base.models import UserEvaluation

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)


        if search_query:
            qset2 =  reduce(operator.__or__, [Q(client__company__icontains=query) for query in search_query])
            user_evaluations = UserEvaluation.objects.filter(qset2, employee=request.user.employee).distinct()

            if filter_query:
                if filter_query == 'on-evaluation':
                    user_evaluations = user_evaluations.filter(percentage=0)
                elif filter_query == 'evaluated':
                    user_evaluations = user_evaluations.exclude(percentage=0)
            
        


            return TemplateResponse(
                request,
                'employee/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                }
            )

        user_evaluations = UserEvaluation.objects.filter(employee=request.user.employee)

        if filter_query:
            if filter_query == 'on-evaluation':
                user_evaluations = user_evaluations.filter(percentage=0)
            elif filter_query == 'evaluated':
                user_evaluations = user_evaluations.exclude(percentage=0)

            

        return TemplateResponse(
                request,
                'employee/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                }
            )

