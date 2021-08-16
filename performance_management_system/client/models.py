
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

        notifications = None

        if name or message or time or status or position:

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(user_evaluation__employee__first_name=query) | Q(user_evaluation__employee__last_name=query) for query in name])
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
            
            

            return JsonResponse(
                data={
                    'html' : render_to_string(
                         'base/search_notifications.html',
                        {
                            'notifications' : self.paginate_data(notifications.order_by('created_at'), page),
                        }
                    ),
                },
            )

        if sort:
            notifications = Notification.objects.filter(reciever=request.user).order_by(sort)
        else:
            notifications = Notification.objects.filter(reciever=request.user).order_by('-created_at')

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
            },
            template="base/notifications_view.html",
        )


    @route(r'^notifications/(\d+)/evaluation/$')
    def notification_evaluation(self, request, notification_id):
        from performance_management_system.base.models import Notification, EvaluationPage, EvaluationCategories

        notification = Notification.objects.get(pk=notification_id)
        user_evaluation = notification.user_evaluation
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
                'current_menu':'notifications',
                'notification_url': self.url,
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
                'search_page': self,
                'notification_url': notification_url,
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

        user_evaluations = None

        if name or address or contact_number or status or sort or position:

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) for query in name])
                user_evaluations = UserEvaluation.objects.filter(qset1, client=request.user.client).distinct()
                if sort:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__status__icontains=status, employee__position__icontains=position).order_by(sort)
                else:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__status__icontains=status, employee__position__icontains=position)
            else:
                if sort:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__status__icontains=status, employee__position__icontains=position, client_id=client_id).order_by(sort)
                else:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__status__icontains=status, employee__position__icontains=position, client_id=client_id)
            
            

            return JsonResponse(
                data={
                    'html' : render_to_string(
                         'client/search_employee_specified.html',
                        {
                            'user_evaluations' : self.paginate_data(user_evaluations, page),
                            'evaluation_page_index': EvaluationPage.objects.live().first()
                        }
                    ),
                },
            )

        user_evaluations = UserEvaluation.objects.filter(client=request.user.client)

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
                            'evaluation_page_index': EvaluationPage.objects.live().first()
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
