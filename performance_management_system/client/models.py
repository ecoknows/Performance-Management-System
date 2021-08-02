
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

from performance_management_system import IntegerResource, StringResource, IS_EVALUATED
from performance_management_system.users.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from itertools import chain
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
                on_evaluation_employee = request.user.client.user_evaluation.filter(percentage=0)
            elif notification.notification_type == 'notify-evaluated-specific-client' or notification.notification_type == 'new-employee-client' or notification.notification_type == 'evaluated-form-is-send-to-employee':
                on_evaluation_employee = notification.user_evaluation

            return JsonResponse(
                data={
                    'selected_html' : render_to_string(
                        'base/selected_notification.html', 
                        {
                            'notification': notification,
                            'selected_hr_admin': selected_hr_admin,
                            'on_evaluation_employee': on_evaluation_employee,
                            'evaluation_index_page': EvaluationPage.objects.live().first().url
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
                            'evaluation_index_page': EvaluationPage.objects.live().first().url+str(selected_user_evaluation.pk)
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
                'user_model' : request.user.client,
                'notifications' : self.paginate_notification(notifications, current_page, 10),
                'notification_url': self.url,
                'menu_lists': [
                    [ClientIndexPage.objects.live().first().url,'Employees']
                ],
                'notifications_count' : len(notifications),
                'search_page': ClientIndexPage.objects.live().first()
            },
            template="base/notifications.html",
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
    
    status = models.CharField(
        max_length=255,
        choices=IS_EVALUATED,
        default='none'
    )
    

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
  

class ClientIndexPage(BaseAbstractPage):
    max_count = 1
    parent_page_types = ['base.BaseIndexPage']
    
    @route(r'^search/$')
    def pop_search(self, request):
        from performance_management_system.base.models import UserEvaluation, EvaluationPage

        search_query = request.GET.get('search_query', None).split()

        if search_query :        
            qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) | Q(employee__position__icontains=query) for query in search_query])

            user_evaluations = UserEvaluation.objects.filter(qset1, client=request.user.client).distinct()

            if len(user_evaluations) == 0:
                return JsonResponse(data={
                    'empty': True
                })

            return TemplateResponse(request, 'client/pop_search.html', {
                'results' : user_evaluations,
                'user_evaluation_details_index' : EvaluationPage.objects.live().first(),
            })
        return JsonResponse(data={
            'empty': True
        })

    def get_menu_list(self):
        return [
            [self.url,'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]

        
    @route(r'^$') 
    def default_route(self, request):
        from performance_management_system.base.models import EvaluationPage
        
        filter_query = request.GET.get('filter', None)
        filter_text = None
        
        if filter_query:
            if filter_query == 'on-evaluation':
                filter_text = 'On Evaluation'
            elif filter_query  == 'evaluated':
                filter_text = 'Evaluated'

        return self.render(
            request,
            context_overrides={
                'menu_lists': self.get_menu_list(),
                'user_model': request.user.client,
                'title': 'EMPLOYEES',
                'evaluation_index': EvaluationPage.objects.live().first().url,
                'search_page': self,
                'filter': filter_text,
                'filter_query': filter_query,
            }
        )
    
    @route(r'^search/employee/$')
    def employee_search(self, request):
        from performance_management_system.base.models import UserEvaluation,EvaluationPage

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)

        user_evaluations = None

        if search_query:
            qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) | Q(employee__position__icontains=query)  for query in search_query])

            user_evaluations = UserEvaluation.objects.filter(qset1, client=request.user.client).distinct()

            if filter_query:
                if filter_query == 'on-evaluation':
                    user_evaluations = user_evaluations.filter(percentage=0)
                elif filter_query == 'evaluated':
                    user_evaluations = user_evaluations.exclude(percentage=0)
            

            return TemplateResponse(
                request,
                'client/search_employee_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                    'evaluation_page_index' : EvaluationPage.objects.live().first()
                }
            )

        user_evaluations = UserEvaluation.objects.filter(client=request.user.client)

        if filter_query:
            if filter_query == 'on-evaluation':
                user_evaluations = user_evaluations.filter(percentage=0, client=request.user.client)
            elif filter_query == 'evaluated':
                user_evaluations = user_evaluations.exclude(percentage=0).filter(client=request.user.client)


        return TemplateResponse(
                request,
                'client/search_employee_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                    'evaluation_page_index' : EvaluationPage.objects.live().first()
                }
            )