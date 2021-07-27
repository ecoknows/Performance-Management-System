from django.db import models
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import SearchVector
from wagtail import search


from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system.base.models import BaseAbstractPage, UserEvaluation, EvaluationCategories, EvaluationPage, Notification
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource, DETAILS_MENU

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
            elif filter_query == 'on-evaluation':
                self.filter  = 'On Evaluation'
                return UserEvaluation.objects.filter(
                    percentage=0,
                    client_id=client_id
                )

        return UserEvaluation.objects.filter(client_id=client_id)

    

    
    @route(r'^$') 
    def default_route(self, request):
        hr_index_url = HRIndexPage.objects.first().url

        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                self.filter = 'Evaluated'
            elif filter_query == 'on-evaluation':
                self.filter = 'On Evaluation'

        menu_lists = [
            (hr_index_url,'Dashboard'),
            [self.url, 'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]
        notification_url = HRIndexPage.objects.live().first().url

        client_id = request.POST.get('client_id', None)

        if client_id:
            client = User.objects.get(pk=client_id)

            Notification.objects.create(
                reciever=client,
                message='Kindly finish the remaining evaluation ',
                hr_admin=request.user.hradmin,
                notification_type='notify-evaluated-all-client'
            )

            user_evaluations = client.client.user_evaluation.filter(percentage=0)
            for user_evaluation in user_evaluations:
                Notification.objects.create(
                    reciever=user_evaluation.employee.user,
                    message='Dear employee, I have now notify ' + user_evaluation.client.company + ' to evaluate all the remaining evaluation',
                    hr_admin=request.user.hradmin,
                    notification_type='client-has-been-notify'
                )
            return JsonResponse(data={
                'message': 'The client has been successfully notified!'
            })

        return self.render(
            request,
            context_overrides={
                'menu_lists': menu_lists,
                'notification_url': notification_url,
                'filter': self.filter,
                'filter_query': filter_query
            }
        )

    @route(r'^(\d+)/$')
    def client_details(self, request, id):
        hr_index_url = HRIndexPage.objects.first().url
        menu_lists = [
            (hr_index_url,'Dashboard'),
            [self.url+id, 'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]
        return self.render(
            request,
            context_overrides={
                'user_evaluations': self.get_assign_employee(request, id),
                'menu_lists': menu_lists,
                'user_model': request.user.hradmin,
                'employee_model': Client.objects.get(pk=id),
                'evaluation_index': 'evaluated/',
                'filter': self.filter
            },
            template='client/client_index_page.html'
        )
    
    @route(r'^(\d+)/evaluated/(\d+)/$')
    def client_details_evaluated(self, request, id, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        hr_index_url = HRIndexPage.objects.first().url

        menu_lists = [
            (hr_index_url,'Dashboard'),
            ['../../','Employees'],
            ['../../../','Client Lists'],
        ]
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'menu_lists': menu_lists,
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate}
            },
            template="base/evaluation_page.html",
        )

    @route(r'^search/$')
    def client_search(self, request):

        search_query = request.GET.get('search_query', None)
        filter_query = request.GET.get('filter', None)

        if search_query:
            clients = Client.objects.filter(company__icontains=search_query)

            
            if filter_query :
                print(filter_query)
                clients = clients.filter( status=filter_query)

            return TemplateResponse(
                request,
                'hr/search_client.html',
                {
                    'clients' : clients
                }
            )

        if filter_query:
            clients = Client.objects.filter(status=filter_query)
        else:
            clients = Client.objects.all()

        return TemplateResponse(
                request,
                'hr/search_client.html',
                {
                    'clients' : clients
                }
            )
        
    
    
    

class EmployeeListPage(RoutablePageMixin,Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']

    def get_menu_list(self):
        hr_index_url = HRIndexPage.objects.first().url
        
        return [
            (hr_index_url,'Dashboard'),
            [self.url, 'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]

    def get_context(self, request):
        context = super(EmployeeListPage, self).get_context(request)
        filter_query = request.GET.get('filter', None)

        if filter_query:
            context['filter_query'] = filter_query
            if filter_query == 'evaluated':
                context['filter'] = 'Evaluated'
            elif filter_query == 'on-evaluation':
                context['filter'] = 'On Evaluation'
            
        context['menu_lists'] = self.get_menu_list()
        context['notification_url'] = HRIndexPage.objects.live().first().url

        return context

    
    @route(r'^search/$')
    def employee_search(self, request):

        search_query = request.GET.get('search_query', None)
        filter_query = request.GET.get('filter', None)

        if search_query:
            employees = Employee.objects.annotate(
                search=SearchVector('first_name','last_name','middle_name')
            ).filter(search__icontains=search_query)

            if filter_query:
                employees = employees.filter( status=filter_query)

            return TemplateResponse(
                request,
                'hr/search_employee.html',
                {
                    'employees' : employees
                }
            )
        if filter_query:
            employees = Employee.objects.filter(status=filter_query)
        else:
            employees = Employee.objects.all()

        return TemplateResponse(
                request,
                'hr/search_employee.html',
                {
                    'employees' : employees
                }
            )



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
    filter = 'All'
    
    def get_clients_not_picked(self, employee):
        return Client.objects.exclude(user_evaluation__employee=employee)

    def get_user_evaluation_picked(self, request, employee):
        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                self.filter = 'Evaluated'
                return UserEvaluation.objects.exclude(percentage=0).filter(employee=employee)
            elif filter_query == 'on-evaluation':
                self.filter = 'On Evaluation'
                return UserEvaluation.objects.filter(employee=employee, percentage=0)

        return UserEvaluation.objects.filter(employee=employee)
        
    
    @route(r'^$') 
    def default_route(self, request):
        return HttpResponseRedirect('../')
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        context['notification_url'] = HRIndexPage.objects.live().first().url
        context['menu_lists'] = [
            ('/'+HRIndexPage.objects.live().first().url, 'Dashboard')
        ]

        return context
    

    @route(r'^(\d+)/$', name='id')
    def details_user_route(self, request, id):
        employee = Employee.objects.get(pk=id)
        categories = EvaluationCategories.objects.all()
        
        menu_lists = [
            [HRIndexPage.objects.live().first().url, 'Dashboard'],
            ['', 'Details'],
            ['clients', 'Clients'],
            ['pick-a-client','Pick a client'],
        ]

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
        user_evaluations = self.get_user_evaluation_picked(request, employee=employee)
        menu_lists = [
            [HRIndexPage.objects.live().first().url, 'Dashboard'],
            ['../', 'Details'],
            ['../pick-a-client','Pick a client'],
            [self.url+id+'/clients','All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]

        
        user_evaluation_id = request.POST.get('user_evaluation_id', None)


        if  user_evaluation_id:
            user_evaluation  = UserEvaluation.objects.get(pk=user_evaluation_id)

            Notification.objects.create(
                reciever=user_evaluation.client.user,
                message='Please Evaluate '+ str(user_evaluation.employee),
                hr_admin=request.user.hradmin,
                user_evaluation= user_evaluation,
                notification_type='notify-evaluated-specific-client'
            )
            Notification.objects.create(
                reciever=user_evaluation.employee.user,
                message='Rest assured I have notify '+ user_evaluation.client.company + ' to evalaute',
                hr_admin=request.user.hradmin,
                user_evaluation= user_evaluation,
                notification_type='client-has-been-notify'
            )
            return JsonResponse(data={
                'message': 'The client has been successfully notified!'
            })


        return self.render(
            request,
            context_overrides={
            'employee_id': id+'/',
            'user_evaluations': user_evaluations,
            'employee': employee,
            'menu_lists': menu_lists,
            'filter': self.filter,
            },
            template="hr/employee_client_list.html",
        )

    @route(r'^(\d+)/clients/(\d+)/$')
    def client_evaluation_details(self, request, id, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        menu_lists = [
            [HRIndexPage.objects.live().first().url, 'Dashboard'],
            ['../../', 'Details'],
            ['../../pick-a-client','Pick a client'],
            ['../','Clients'],
        ]
        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'menu_lists': menu_lists,
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
        menu_lists = [
            [HRIndexPage.objects.live().first().url, 'Dashboard'],
            ['../', 'Details'],
            ['../clients','Clients'],
        ]
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
        user_evaluation = UserEvaluation.objects.create(
            employee_id=employee_id,
            client_id=client_id,
            hr_admin=request.user
        )
        
        employee = Employee.objects.get(pk=employee_id)
        employee.status = 'on-evaluation'

        client = Client.objects.get(pk=client_id)
        client.status = 'on-evaluation'

        Notification.objects.create(
            reciever=client.user,
            hr_admin=request.user.hradmin,
            message='A new employee have been assign',
            user_evaluation=user_evaluation,
            notification_type='new-employee-client'
        )

        Notification.objects.create(
            reciever=employee.user,
            hr_admin=request.user.hradmin,
            message='A new client have been assign',
            user_evaluation=user_evaluation,
            notification_type='new-client-employee'
        )

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

        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()

        context['employee_list_index'] = employee_list_index
        context['client_list_index'] = client_list_index
        context['menu_lists'] = [
            [employee_list_index.url, 'Employees'],
            [client_list_index.url, 'Clients']
        ]

        return context
    