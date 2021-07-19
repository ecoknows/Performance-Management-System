from django.db import models
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system.base.models import BaseAbstractPage, UserEvaluation, EvaluationCategories, EvaluationPage
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource, LIST_MENU, DETAILS_MENU

class ClientListPage(RoutablePageMixin,Page):
    max_count = 1
    filter = None
    parent_page_types = ['HRIndexPage']
    
    def get_assign_employee(self, request, client_id):
        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                self.filter = 'Evaluated'
                return UserEvaluation.objects.exclude(percentage=0).filter(
                    client_id=client_id
                )
            elif filter_query == 'on evaluation':
                self.filter  = 'On Evaluation'
                return UserEvaluation.objects.filter(
                    percentage=0,
                    client_id=client_id
                )

        return UserEvaluation.objects.filter(client_id=client_id)

    def get_clients(self, request):
        # filter_query = request.GET.get('filter', None)
        
        # if filter_query:
        #     if filter_query == 'evaluated':
        #         context['filter'] = 'Evaluated'
        #     elif filter_query == 'on-evaluation':
        #         context['filter'] = 'on-evaluation'
        #     return Employee.objects.filter(status=filter_query)

        return Client.objects.all()
    
    def get_menu_list(self):
        return LIST_MENU

    
    @route(r'^(\d+)/$')
    def client_details(self, request, id):
        
        return self.render(
            request,
            context_overrides={
                'user_evaluations': self.get_assign_employee(request, id),
                'menu_lists': self.get_menu_list(),
                'user_model': request.user.hradmin,
                'employee_model': Client.objects.get(pk=id),
                'evaluation_index': 'evaluated/'
            },
            template='client/client_index_page.html'
        )
    
    @route(r'^(\d+)/evaluated/(\d+)/$')
    def client_details_evaluated(self, request, id, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate}
            },
            template="base/evaluation_page.html",
        )
        
    
    
    def get_context(self, request):
        context = super(ClientListPage, self).get_context(request)

        context['clients'] = self.get_clients(request)
        context['menu_lists'] = self.get_menu_list()
        context['notification_url'] = HRIndexPage.objects.live().first().url
        return context
    

class EmployeeListPage(Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']
    
    def get_employees(self, request, context):
        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                context['filter'] = 'Evaluated'
            elif filter_query == 'on-evaluation':
                context['filter'] = 'On Evaluation'
            return Employee.objects.filter(status=filter_query)

        return Employee.objects.all()

    def get_menu_list(self):
        return LIST_MENU

    def get_context(self, request):
        context = super(EmployeeListPage, self).get_context(request)

        context['employees'] = self.get_employees(request, context)
        context['menu_lists'] = self.get_menu_list()
        context['notification_url'] = HRIndexPage.objects.live().first().url

        return context



class ClientDetailsPage( Page):
    max_count = 1
    def serve(self, request):
        
        if "query" in request.GET:
            try:
                return render(request, self.template,{
                    'client': Client.objects.get(pk=request.GET['query'])
                })
            except Client.DoesNotExist:
                return redirect('/')
            
        
        return super().serve(request)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['notification_url'] = HRIndexPage.objects.live().first().url
        return context

    
    parent_page_types = ['ClientListPage']




class EmployeeDetailsPage(RoutablePageMixin, Page):
    max_count = 1
    
    def get_clients_not_picked(self, employee):
        return Client.objects.exclude(user_evaluation__employee=employee)

    def get_user_evaluation_picked(self, employee):
        return UserEvaluation.objects.filter(employee=employee)
        
    def get_menu_list(self):
        return DETAILS_MENU

    
    @route(r'^$') 
    def default_route(self, request):
        return HttpResponseRedirect('../')
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context['notification_url'] = HRIndexPage.objects.live().first().url

        return context
    

    @route(r'^(\d+)/$', name='id')
    def details_user_route(self, request, id):
        employee = Employee.objects.get(pk=id)
        categories = EvaluationCategories.objects.all()
        
        menu_lists = self.get_menu_list()
        return self.render(
            request,
            context_overrides={
            'categories': categories,
            'employee_id': id+'/',
            'employee': employee,
            'user_model': request.user.hradmin ,
            'menu_lists': menu_lists
            }
        )
    
    @route(r'^(\d+)/clients/$', name='id')
    def client_list(self, request, id):
        employee = Employee.objects.get(pk=id)
        user_evaluations = self.get_user_evaluation_picked(employee=employee)
        edited_menu_list = self.get_menu_list()
        menu_lists = edited_menu_list
        return self.render(
            request,
            context_overrides={
            'employee_id': id+'/',
            'user_evaluations': user_evaluations,
            'employee': employee,
            'menu_lists': menu_lists,
            },
            template="hr/employee_client_list.html",
        )

    @route(r'^(\d+)/clients/(\d+)/$')
    def client_evaluation_details(self, request, id, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate}
            },
            template="base/evaluation_page.html",
        )

    @route(r'^(\d+)/pick-a-client/$')
    def pick_a_client(self, request, id):
        employee = Employee.objects.get(pk=id)
        clients = self.get_clients_not_picked(employee=employee)
        menu_lists = self.get_menu_list()
        return self.render(
            request,
            context_overrides={
            'employee_id': id+'/',
            'clients': clients,
            'employee': employee,
            'menu_lists': menu_lists,
            },
            template="hr/pick_client_page.html",
        )
        
    @route(r'^(\d+)/pick-a-client/add/(\d+)/$')
    def add_a_client(self, request, employee_id, client_id):
        UserEvaluation.objects.get_or_create(
            employee_id=employee_id,
            client_id=client_id
        )
        
        employee = Employee.objects.get(pk=employee_id)
        employee.status = 'on-evaluation'

        client = Client.objects.get(pk=client_id)
        client.status = 'on-evaluation'

        employee.save()
        client.save()
        
        return HttpResponseRedirect('../../')

    parent_page_types = ['EmployeeListPage']


class HrAdmin(models.Model):
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
    last_name = models.CharField(max_length=25, null=True)
    
    panels = [
        ImageChooserPanel('profile_pic'),
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('middle_name'),
            FieldPanel('last_name'),    
        ], heading='HR Admin Complete Name'),
    ]
    
    @property
    def hr_id(self):
        id = str(IntegerResource.HR_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    @property
    def hr_admin(self):
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
        return self.hr_admin

    def delete(self):
        if self.user:
            self.user.delete()
        super().delete()


class HRIndexPage(BaseAbstractPage):
    max_count = 1
    parent_page_types = ['base.BaseIndexPage']
    

    def get_context(self, request):
        context = super(HRIndexPage, self).get_context(request)

        context['evaluated_employee'] = len(Employee.objects.filter(status='evaluated'))
        context['evaluated_client'] = len(Client.objects.filter(status='evaluated'))

        
        context['on_evaluation_employee'] = len(Employee.objects.filter(status='on-evaluation'))
        context['on_evaluation_client'] = len(Client.objects.filter(status='on-evaluation'))

        context['employee_list_index'] = EmployeeListPage.objects.live().first()
        context['client_list_index'] = ClientListPage.objects.live().first()

        return context
    