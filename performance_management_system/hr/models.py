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
from django.db.models import Q

from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail import search
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system.base.models import BaseAbstractPage, UserEvaluation, EvaluationCategories, EvaluationPage, Notification, EvaluationRateAssign
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource, DETAILS_MENU

from itertools import chain
import operator
from functools import reduce

class ClientListPage(RoutablePageMixin,Page):
    max_count = 1

    parent_page_types = ['HRIndexPage']
    
    
    @route(r'^$') 
    def default_route(self, request):
        hr_index_url = HRIndexPage.objects.first().url

        filter_query = request.GET.get('filter', None)
        filter_text = None
        

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

        if filter_query:
            if filter_query == 'on-evaluation':
                filter_text = 'On Evaluation'
            elif filter_query  == 'evaluated':
                filter_text = 'Evaluated'

        return self.render(
            request,
            context_overrides={
                'menu_lists': menu_lists,
                'notification_url': notification_url,
                'filter': filter_text,
                'filter_query': filter_query,
                'search_page': self
            }
        )

    @route(r'^(\d+)/$')
    def client_details(self, request, id):
        hr_index_url = HRIndexPage.objects.first().url
        
        filter_query = request.GET.get('filter', None)
        filter_text = None

        if filter_query:
            if filter_query == 'on-evaluation':
                filter_text = 'On Evaluation'
            elif filter_query  == 'evaluated':
                filter_text = 'Evaluated'
        
        menu_lists = [
            (hr_index_url,'Dashboard'),
            [self.url+id, 'All'],
            ['?filter=evaluated','Evaluated'],
            ['?filter=on-evaluation','On Evaluation'],
        ]
        return self.render(
            request,
            context_overrides={
                'menu_lists': menu_lists,
                'user_model': request.user.hradmin,
                'employee_model': Client.objects.get(pk=id),
                'evaluation_index': 'evaluated/',
                'filter': filter_text,
                'filter_query': filter_query,
                'client_id': id,
                'search_page': ClientListPage.objects.live().first(),
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
                'self': {'evaluation_max_rate': evaluation_max_rate},
                'search_page': HRIndexPage.objects.live().first(),
            },
            template="base/evaluation_page.html",
        )

    
    @route(r'^search/employee/$')
    def employee_search(self, request):

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)
        client_id = request.GET.get('client_id', None)

        user_evaluations = None

        if search_query:
            qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) | Q(employee__position__icontains=query)  for query in search_query])

            user_evaluations = UserEvaluation.objects.filter(qset1, client_id=client_id).distinct()

            if filter_query:
                if filter_query == 'on-evaluation':
                    user_evaluations = user_evaluations.filter(percentage=0)
                elif filter_query == 'evaluated':
                    user_evaluations = user_evaluations.exclude(percentage=0)
            

            return TemplateResponse(
                request,
                'hr/search_employee_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                }
            )

        user_evaluations = UserEvaluation.objects.filter(client_id=client_id)

        if filter_query:
            if filter_query == 'on-evaluation':
                user_evaluations = user_evaluations.filter(percentage=0, client_id=client_id)
            elif filter_query == 'evaluated':
                user_evaluations = user_evaluations.exclude(percentage=0).filter(client_id=client_id)


        return TemplateResponse(
                request,
                'hr/search_employee_specified.html',
                {
                    'user_evaluations' : user_evaluations,
                }
            )

    @route(r'^search/$')
    def client_search(self, request):

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)
        user_filter_exclude = request.GET.get('user_filter_exclude', None)
        employee = None
        if search_query:
            qset1 =  reduce(operator.__or__, [Q(company__icontains=query) for query in search_query])
            clients = Client.objects.filter(qset1).distinct()
            
            if filter_query:
                if filter_query == 'evaluated':
                    clients = clients.filter( status=filter_query)
                elif filter_query == 'on-evaluation':
                    clients = clients.filter( status=filter_query)
            
            if user_filter_exclude:
                clients = clients.exclude(user_evaluation__employee_id=user_filter_exclude)
                employee = Employee.objects.get(pk=user_filter_exclude)

            return TemplateResponse(
                request,
                'hr/search_client.html',
                {
                    'clients' : clients,
                    'user_filter_exclude': user_filter_exclude,
                    'employee': employee
                }
            )

        clients = Client.objects.all()

        if filter_query == 'evaluated':
            clients = clients.filter( status=filter_query)
        elif filter_query == 'on-evaluation':
            clients = clients.filter( status=filter_query)
        
        if user_filter_exclude:
            clients = clients.exclude(user_evaluation__employee_id=user_filter_exclude)
            employee = Employee.objects.get(pk=user_filter_exclude)

        return TemplateResponse(
                request,
                'hr/search_client.html',
                {
                    'clients' : clients,
                    'user_filter_exclude': user_filter_exclude,
                    'employee': employee
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
        context['search_page'] = self

        return context

    
    @route(r'^search/$')
    def employee_search(self, request):

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)


        if search_query:
            qset1 =  reduce(operator.__or__, [Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(position__icontains=query) for query in search_query])
            employees = Employee.objects.filter(qset1).distinct()

            if filter_query == 'evaluated':
                employees = employees.filter( status=filter_query)
            elif filter_query == 'on-evaluation':
                employees = employees.filter( status=filter_query)

            return TemplateResponse(
                request,
                'hr/search_employee.html',
                {
                    'employees' : employees,
                }
            )
        employees = Employee.objects.all()

        if filter_query == 'evaluated':
            employees = employees.filter( status=filter_query)
        elif filter_query == 'on-evaluation':
            employees = employees.filter( status=filter_query)


        return TemplateResponse(
                request,
                'hr/search_employee.html',
                {
                    'employees' : employees,
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
    
    def get_clients_not_picked(self, employee):
        return Client.objects.exclude(user_evaluation__employee=employee)
        
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
            'categories': categories[:7],
            'infinite_categories': categories[7:],
            'employee_id': id+'/',
            'employee': employee,
            'user_model': request.user.hradmin ,
            'menu_lists': menu_lists,
            'search_page': HRIndexPage.objects.live().first()
            }
        )
    
    @route(r'^(\d+)/clients/$', name='id')
    def client_list(self, request, id):
        employee = Employee.objects.get(pk=id)
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
            try:
                user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
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
            except UserEvaluation.DoesNotExist:
                user_evaluation

                
        
        filter_query = request.GET.get('filter', None)
        filter_text = None
        
        if filter_query:
            if filter_query == 'on-evaluation':
                filter_text = 'On Evaluation'
            elif filter_query  == 'evaluated':
                filter_text = 'Evaluated'
            

        categories = EvaluationCategories.objects.all()
        category_percentages = []
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        
        try:
            latest_evaluation = UserEvaluation.objects.filter(employee=employee).latest('assigned_date')

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
            'employee': employee,
            'menu_lists': menu_lists,
            'filter': filter_text,
            'filter_query': filter_query,
            'search_page': self,
            'latest_evaluation': latest_evaluation,
            'categories': categories,
            'category_percentages': category_percentages,
            'employee_id': id,
            },
            template="hr/employee_client_list.html",
        )

    @route(r'^(\d+)/clients/(\d+)/$')
    def client_evaluation_details(self, request, id, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation
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
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'search_page': HRIndexPage.objects.live().first(),
            },
            template="base/evaluation_page.html",
        )

    @route(r'^(\d+)/pick-a-client/$')
    def pick_a_client(self, request, id):
        
        menu_lists = [
            [HRIndexPage.objects.live().first().url, 'Dashboard'],
            ['../', 'Details'],
            ['../clients','Clients'],
        ]
        return self.render(
            request,
            context_overrides={
            'employee_id': id,
            'employee': Employee.objects.get(pk=id),
            'menu_lists': menu_lists,
            'user_filter_exclude': id,
            'search_page': self,
            },
            template="hr/pick_client_page.html",
        )
        
    @route(r'^(\d+)/pick-a-client/add/$')
    def add_a_client(self, request, employee_id):
        client_id = request.POST.get('client_id', None)
        project_assign = request.POST.get('project_assign', None)

        if client_id:
            user_evaluation = UserEvaluation.objects.create(
                employee_id=employee_id,
                client_id=client_id,
                hr_admin=request.user,
                project_assign=project_assign
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
        
        return JsonResponse(data={'message': 'Successfull'})

    parent_page_types = ['EmployeeListPage']


    @route(r'^search/$')
    def client_search_specified(self, request):

        search_query = request.GET.get('search_query', None).split()
        filter_query = request.GET.get('filter_query', None)
        employee_id = request.GET.get('employee_id', None)
        latest_evaluation_id = request.GET.get('latest_evaluation_id', None)

        user_evaluations = None

        if search_query:
            qset2 =  reduce(operator.__or__, [Q(client__company__icontains=query) for query in search_query])
            user_evaluations = UserEvaluation.objects.filter(qset2, employee_id=employee_id).distinct()

            if filter_query:
                if filter_query == 'on-evaluation':
                    user_evaluations = user_evaluations.filter(percentage=0)
                elif filter_query == 'evaluated':
                    user_evaluations = user_evaluations.exclude(percentage=0)
            
        


            return TemplateResponse(
                request,
                'hr/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations.exclude(pk=latest_evaluation_id),
                }
            )

        user_evaluations = UserEvaluation.objects.filter(employee_id=employee_id)

        if filter_query:
            if filter_query == 'on-evaluation':
                user_evaluations = user_evaluations.filter(percentage=0)
            elif filter_query == 'evaluated':
                user_evaluations = user_evaluations.exclude(percentage=0)

        return TemplateResponse(
                request,
                'hr/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations.exclude(pk=latest_evaluation_id),
                }
            )
    
    @route(r'^search/pick_client/$')
    def pick_client_search(self, request):

        search_query = request.GET.get('search_query', None).split()
        employee_id = request.GET.get('employee_id', None)
        employee = Employee.objects.get(pk=employee_id)

        if search_query:
            qset2 =  reduce(operator.__or__, [Q(company__icontains=query) for query in search_query])
            clients = Client.objects.exclude(user_evaluation__employee_id=employee_id).filter(qset2).distinct()

            
            return TemplateResponse(
                request,
                'hr/search_pick_client.html',
                {
                    'clients' : clients,
                    'employee': employee,
                }
            )

        clients = Client.objects.exclude(user_evaluation__employee_id=employee_id)

        
        return TemplateResponse(
                request,
                'hr/search_pick_client.html',
                {
                    'clients' : clients,
                    'employee': employee,
                }
            )


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
        return self.user.username
    
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

    @route(r'^search/$')
    def pop_search(self, request):

        search_query = request.GET.get('search_query', None).split()

        if search_query :        
            qset1 =  reduce(operator.__or__, [Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(position__icontains=query) for query in search_query])
            qset2 =  reduce(operator.__or__, [Q(company__icontains=query) for query in search_query])

            employees = Employee.objects.filter(qset1).distinct()
            clients = Client.objects.filter(qset2).distinct()

            results = list(chain(employees, clients))

            if len(results) == 0:
                return JsonResponse(data={
                    'empty': True
                })

        
            return TemplateResponse(request, 'base/pop_search.html', {
                'results' : results,
                'employee_details_index': EmployeeDetailsPage.objects.live().first(),
                'client_details_index': ClientListPage.objects.live().first()
            })
        return JsonResponse(data={
            'empty': True
        })
    
    

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
        context['search_page'] = self

        return context
    