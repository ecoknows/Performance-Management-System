
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

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


class BaseAbstractPage(RoutablePageMixin, Page):
    
    @route(r'^notifications/$')
    def notification(self, request):
        from performance_management_system.base.models import Notification, UserEvaluation, EvaluationCategories,EvaluationPage,EvaluationRateAssign

        user_model = None
        if request.user.is_employee:
            user_model = request.user.employee
        if request.user.is_client:
            user_model = request.user.client
        if request.user.is_hr:
            user_model = request.user.hradmin
        
        notifications = Notification.objects.filter(reciever=request.user).order_by('-created_at')

        user_evaluation_id = request.GET.get('user_evaluation_id', None)
        notification_id = request.GET.get('notification_id', None)

        if user_evaluation_id:
            from performance_management_system.hr.models import EmployeeDetailsPage
            if notification_id: 
                notification = Notification.objects.get(pk=notification_id)
                notification.seen = True
                notification.save()
            
            selected_user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)

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
                            'selected_user_evaluation' : selected_user_evaluation,
                            'selected_employee': selected_user_evaluation.employee,
                            'selected_profile_pic': selected_user_evaluation.employee.profile_pic,
                            'selected_position': selected_user_evaluation.employee.position,
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

        return self.render(
            request,
            context_overrides={
                'user_model' : user_model,
                'notifications' : notifications,
                'notifications_count' : len(notifications),
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
        id = str(IntegerResource.CLIENT_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
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

    def get_menu_list(self):
        return []

    def get_assign_employee(self, request, context):
        from performance_management_system.base.models import UserEvaluation
        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                context['filter'] = 'Evaluated'
                return UserEvaluation.objects.exclude(percentage=0).filter(
                    client=request.user.client
                )
            elif filter_query == 'on evaluation':
                context['filter'] = 'On Evaluation'
                return UserEvaluation.objects.filter(
                    percentage=0,
                    client=request.user.client
                )

        return UserEvaluation.objects.filter(client=request.user.client)
        
    def get_context(self, request):
        context = super(ClientIndexPage, self).get_context(request)

        from performance_management_system.base.models import EvaluationPage

        context['user_evaluations'] = self.get_assign_employee(request, context)
        context['menu_lists'] = self.get_menu_list()
        context['user_model'] = request.user.client
        context['title'] = 'EMPLOYEES'
        context['evaluation_index'] = EvaluationPage.objects.live().first().url

        return context