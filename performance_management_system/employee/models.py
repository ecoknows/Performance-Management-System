
from django.db import models
from django.http import JsonResponse
from django.template.loader import render_to_string

from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from performance_management_system import IS_EVALUATED
from performance_management_system.users.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
                'user_model' : request.user.employee,
                'notification_url': self.url,
                'reports_index': ReportsEmployee.objects.live().first()
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
            if sort:
                notifications = Notification.objects.filter(user_evaluation__client__company__icontains=name, message__icontains=message, created_at__icontains=time, seen__icontains=status, reciever=request.user).order_by(sort)
            else:
                notifications = Notification.objects.filter(user_evaluation__client__company__icontains=name, message__icontains=message, created_at__icontains=time, seen__icontains=status, reciever=request.user)
            

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
                'user_model' : request.user.employee,
                'notification_url': self.url,
                'notification': notification,
                'categories' : categories,
                'category_percentages': category_percentages,
                'reports_index': ReportsEmployee.objects.live().first()
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
                'user_model' : request.user.employee,
                'employee_model': user_evaluation.employee,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'notifications',
                'notification_url': self.url,
                'reports_index': ReportsEmployee.objects.live().first()
            },
            template="base/evaluation_page.html",
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

class ReportsEmployee(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ['EmployeeIndexPage']

    @route(r'^$') 
    def default_route(self, request):
        
        return self.render(
            request,
            context_overrides={
                'user_model': request.user.employee,
                'notification_url' : EmployeeIndexPage.objects.live().first().url ,
                'reports_index': self,
            })

class EmployeeIndexPage(BaseAbstractPage):
    max_count = 1
    parent_page_types = ['base.BaseIndexPage']

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
            'current_menu':'dashboard',
            'reports_index': ReportsEmployee.objects.live().first()
            },
            template='hr/employee_details_page.html'
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
                'current_menu':'dashboard',
                'reports_index': ReportsEmployee.objects.live().first()
            },
            template="base/evaluation_page.html",
        )