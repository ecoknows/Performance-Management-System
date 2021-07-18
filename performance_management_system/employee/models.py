
from django.db import models
from django.utils import timezone
from wagtail.core.models import Page

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from performance_management_system import IntegerResource, StringResource, DETAILS_MENU_EMPLOYEE, IS_EVALUATED, DETAILS_MENU_EMPLOYEE_CLIENTS
from performance_management_system.users.models import User


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
        id = str(IntegerResource.EMPLOYEE_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
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
            
    
class EmployeeIndexPage(RoutablePageMixin,Page):
    max_count = 1
    filter = None

    def get_menu_list(self):
        return DETAILS_MENU_EMPLOYEE

    def get_user_evaluation(self, request, employee):
        from performance_management_system.base.models import UserEvaluation
        
        filter_query = request.GET.get('filter', None)
        print(filter_query, 'HEYO')
        
        if filter_query:
            if filter_query == 'evaluated':
                self.filter = 'Evaluated'
                return UserEvaluation.objects.exclude(percentage=0).filter(employee=employee)
            elif filter_query == 'on-evaluation':
                self.filter = 'On Evaluation'
                return UserEvaluation.objects.filter(employee=employee, percentage=0)

        return UserEvaluation.objects.filter(employee=employee)

    @route(r'^$')
    def dash_board(self, request):
        from performance_management_system.base.models import EvaluationCategories
        id = request.user.employee.pk
        categories = EvaluationCategories.objects.all()
        
        menu_lists = self.get_menu_list()
        return self.render(
            request,
            context_overrides={
            'categories': categories,
            'employee_id': str(id)+'/',
            'menu_lists': menu_lists,
            'user_model': request.user.employee,
            },
            template='hr/employee_details_page.html'
        )
    
    @route(r'^clients/$')
    def client_list(self, request):
        user_evaluations = self.get_user_evaluation(request, employee=request.user.employee)
        return self.render(
            request,
            context_overrides={
                'user_evaluations': user_evaluations,
                'filter': self.filter,
                'menu_lists': DETAILS_MENU_EMPLOYEE_CLIENTS
            },
            template='employee/client_list.html'
        )
    
    @route(r'clients/(\d+)/$')
    def client_evaluation_details(self, request, user_evaluation_id):
        from performance_management_system.base.models import UserEvaluation, EvaluationPage, EvaluationCategories

        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.employee,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate}
            },
            template="base/evaluation_page.html",
        )

