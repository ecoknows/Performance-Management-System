from django.db import models
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils import timezone

from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system.base.models import BaseAbstractPage, UserEvaluation, EvaluationCategories, EvaluationPage, Notification, EvaluationRateAssign
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client
from performance_management_system.users.models import User

import operator
from functools import reduce
import pytz

class ClientListPage(RoutablePageMixin,Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']

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


        client_id = request.POST.get('client_id', None)

        if client_id:
            client = User.objects.get(pk=client_id)
            client_remaining_eval = client.client.user_evaluation.filter(submit_date__isnull=True)
            
            client_message = 'Kindly finish your ' +  str(len(client_remaining_eval)) + ' remaining evaluation'

            notification_client = Notification.objects.create(
                reciever=client,
                message=client_message,
                hr_admin=request.user.hradmin,
                notification_type='notify-evaluated-all-client'
            )

            user_evaluations = client.client.user_evaluation.filter(submit_date__isnull=True)
            for user_evaluation in user_evaluations:
                Notification.objects.create(
                    reciever=user_evaluation.employee.user,
                    message='Dear employee, I have now notify ' + user_evaluation.client.company + ' to evaluate all the remaining evaluation',
                    hr_admin=request.user.hradmin,
                    notification_type='client-has-been-notify'
                )

            return JsonResponse(data={
                'message': 'The client has been successfully notified!',
                'created_at': notification_client.created_at,
            })


        return self.render(
            request,
            context_overrides={
                'client_list_index': self,
                'notification_url': HRIndexPage.objects.live().first().url,
                'employee_list_index': EmployeeListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': ReportsHR.objects.live().first(),
            }
        )

    @route(r'^(\d+)/$')
    def client_details(self, request, id):

        user_evaluation_id = request.POST.get('user_evaluation_id', None)

        if user_evaluation_id:
            user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
            notification_client = Notification.objects.create(
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
                'message': 'The employee has been successfully notified!',
                'created_at': notification_client.created_at,
            })

        return self.render(
            request,
            context_overrides={
                'user_model': request.user.hradmin,
                'client_model': Client.objects.get(pk=id),
                'client_id': id,
                'notification_url': HRIndexPage.objects.live().first().url,
                'client_list_index': self,
                'employee_list_index': EmployeeListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': ReportsHR.objects.live().first(),
                'current_menu' : 'clients'
            },
            template='hr/client_details_page.html'
        )
    
    @route(r'^(\d+)/evaluated/(\d+)/$')
    def client_details_evaluated(self, request, id, user_evaluation_id):
        evaluation_page =  EvaluationPage.objects.live().first()
        evaluation_max_rate = evaluation_page.evaluation_max_rate
        legend_evaluation = evaluation_page.legend_evaluation

        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        hr_index_url = HRIndexPage.objects.first().url
        notification_url = HRIndexPage.objects.live().first().url

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
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'notification_url': notification_url,
                'client_list_index': self,
                'current_menu' : 'clients',
                'employee_list_index': EmployeeListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': ReportsHR.objects.live().first(),
            },
            template="base/evaluation_page.html",
        )

    @route(r'^(\d+)/search/employees/$')
    def employee_search(self, request, client_id):

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        user_evaluations = None

        if name or address or contact_number or status or sort or position:

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) for query in name])
                user_evaluations = UserEvaluation.objects.filter(qset1, client_id=client_id).distinct()
                if sort:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position).order_by(sort)
                else:
                    user_evaluations = user_evaluations.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position)
            else:
                if sort:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position, client_id=client_id).order_by(sort)
                else:
                    user_evaluations = UserEvaluation.objects.filter( employee__address__icontains=address, employee__contact_number__icontains=contact_number, employee__position__icontains=position, client_id=client_id)
            
            if status == 'for-evaluation':
                user_evaluations = user_evaluations.filter( submit_date__isnull=True)
            if status == 'done-evaluating':
                user_evaluations = user_evaluations.filter( submit_date__isnull=False)


        else:
            if sort:
                user_evaluations = UserEvaluation.objects.filter(client_id=client_id).order_by(sort)
            else:
                user_evaluations = UserEvaluation.objects.filter(client_id=client_id).order_by('-submit_date','assigned_date')
            

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
                        'hr/search_employee_specified.html',
                        {
                            'user_evaluations' : user_evaluations,
                            'timezone': timezone,
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

    @route(r'^search/clients/$')
    def client_search(self, request):

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        employee = None
        if name or address or contact_number or status or sort:
            if sort:
                clients = Client.objects.filter(company__icontains=name, address__icontains=address, contact_number__icontains=contact_number).order_by(sort)
            else:
                clients = Client.objects.filter(company__icontains=name, address__icontains=address, contact_number__icontains=contact_number)
            
            if status == 'for-evaluation':
                clients = clients.filter( user_evaluation__submit_date__isnull=True)
            if status == 'done-evaluating':
                clients = clients.exclude( user_evaluation__submit_date__isnull=True)
            if status == 'none':
                clients = clients.filter( user_evaluation=None)
        else:
            if sort:
                clients = Client.objects.all().order_by(sort)
            else:
                clients = Client.objects.all()

        clients = self.paginate_data(clients, page)
        max_pages = clients.paginator.num_pages
        starting_point = clients.number
        next_number = 1
        previous_number = 1

        if clients.has_next():
            next_number = clients.next_page_number()
        
        if clients.has_previous():
            previous_number = clients.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 


        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'hr/search_client.html',
                        {
                            'clients' : clients,
                            'employee': employee,
                            'timezone': timezone,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': clients,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': clients.number,
                },
            )
        
class EmployeeListPage(RoutablePageMixin,Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']
    
    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 7)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^$') 
    def default_route(self, request):
        employee_id = request.POST.get('employee_id', None)
        action = request.POST.get('action', None)

        if employee_id:
            if action == 'notify':
                employee = User.objects.get(pk=employee_id)

                notification_client = Notification.objects.create(
                    reciever=employee,
                    message='Dear employee, kindly wait you evaluation, we have notify already your current client',
                    hr_admin=request.user.hradmin,
                    user_evaluation=employee.employee.current_user_evaluation,
                    notification_type='client-has-been-notify'
                )

                return JsonResponse(data={
                    'message': 'The employee has been successfully notified!',
                    'created_at': notification_client.created_at,
                })
            elif action == 'end_contract':
                user = User.objects.get(pk=employee_id)
                user.employee.current_user_evaluation = None
                user.employee.save()    



        return self.render(
            request,
            context_overrides={
                'notification_url': HRIndexPage.objects.live().first().url,
                'employee_list_index': self,
                'client_list_index':  ClientListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': ReportsHR.objects.live().first(),
            }
        )

    @route(r'^search/employees/$')
    def employee_search(self, request):


        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        position = request.GET.get('position', '')
        status = request.GET.get('status', '')
        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')


        if name or address or contact_number or status or sort or position:
            employees = None

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(first_name__icontains=query) | Q(last_name__icontains=query) for query in name])
                employees = Employee.objects.filter(qset1).distinct()

                if sort:
                    employees = employees.filter( address__icontains=address, contact_number__icontains=contact_number, position__icontains=position).order_by(sort)
                else:
                    employees = employees.filter( address__icontains=address, contact_number__icontains=contact_number, position__icontains=position)
                
            else:
                if sort:
                    employees = Employee.objects.filter( address__icontains=address, contact_number__icontains=contact_number, position__icontains=position).order_by(sort)
                else:
                    employees = Employee.objects.filter( address__icontains=address, contact_number__icontains=contact_number, position__icontains=position)

            if status == 'for-evaluation':
                employees = employees.filter( current_user_evaluation__isnull=False, current_user_evaluation__submit_date__isnull=True)
            if status == 'done-evaluating':
                employees = employees.filter( current_user_evaluation__submit_date__isnull=False)
            if status == 'none':
                employees = employees.filter( current_user_evaluation=None)

        else:
            if sort:
                employees = Employee.objects.all().order_by(sort)
            else:
                employees = Employee.objects.all()


        employees = self.paginate_data(employees, page)
        max_pages = employees.paginator.num_pages
        starting_point = employees.number
        next_number = 1
        previous_number = 1

        if employees.has_next():
            next_number = employees.next_page_number()
        
        if employees.has_previous():
            previous_number = employees.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 


        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'hr/search_employee.html',
                        {
                            'employee_details_index': EmployeeDetailsPage.objects.live().first().url,
                            'employees' : employees,
                            'timezone': timezone,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': employees,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': employees.number,
                },
            )

class EmployeeDetailsPage(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ['EmployeeListPage']
        
    @route(r'^$') 
    def default_route(self, request):
        return HttpResponseRedirect('../')

    @route(r'^(\d+)/$', name='id')
    def details_user_route(self, request, id):
        employee = Employee.objects.get(pk=id)
        user_evaluation = employee.current_user_evaluation
        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []
        overall_performance = 0


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
            
            overall_performance = overall_performance + percentage
            
            category_percentages.append([category,percentage])

        if overall_performance != 0:
            overall_performance = overall_performance / len(categories)
            
        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()
        assign_employee_index = AssignEmployee.objects.live().first()
        
        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'user_model': request.user.hradmin ,
            'category_percentages': category_percentages,
            'current_menu':'employees',
            'assign_employee_index': assign_employee_index,
            'employee_list_index': employee_list_index,
            'client_list_index': client_list_index,
            'notification_url': HRIndexPage.objects.live().first().url,
            'reports_index': ReportsHR.objects.live().first(),
            'max_rate' : max_rate,
            'overall_performance': overall_performance,
            'employee': employee,
            }
        )
    
    @route(r'^(\d+)/clients/$', name='id')
    def client_list(self, request, id):
        employee = Employee.objects.get(pk=id)

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
            'latest_evaluation': latest_evaluation,
            'categories': categories,
            'category_percentages': category_percentages,
            'employee_id': id,
            },
            template="hr/employee_client_list.html",
        )

    @route(r'^(\d+)/evaluation/$')
    def client_evaluation_details(self, request, id):
        employee = Employee.objects.get(pk=id)
        user_evaluation = employee.current_user_evaluation
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation

        
        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()
        assign_employee_index = AssignEmployee.objects.live().first()

        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'employees',
                'assign_employee_index': assign_employee_index,
                'employee_list_index': employee_list_index,
                'client_list_index': client_list_index,
                'notification_url': HRIndexPage.objects.live().first().url,
                'reports_index': ReportsHR.objects.live().first(),
            },
            template="base/evaluation_page.html",
        )

    @route(r'^search/$')
    def client_search_specified(self, request):

        search_query = request.GET.get('search_query', None).split()
        employee_id = request.GET.get('employee_id', None)
        latest_evaluation_id = request.GET.get('latest_evaluation_id', None)

        user_evaluations = None

        if search_query:
            qset2 =  reduce(operator.__or__, [Q(client__company__icontains=query) for query in search_query])
            user_evaluations = UserEvaluation.objects.filter(qset2, employee_id=employee_id).distinct()
        


            return TemplateResponse(
                request,
                'hr/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations.exclude(pk=latest_evaluation_id),
                }
            )

        user_evaluations = UserEvaluation.objects.filter(employee_id=employee_id)

        return TemplateResponse(
                request,
                'hr/search_client_specified.html',
                {
                    'user_evaluations' : user_evaluations.exclude(pk=latest_evaluation_id),
                }
            )

class AssignEmployee(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']

    
    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 7)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^$') 
    def default_route(self, request):
        
        employee_id = request.POST.get('employee_id', None)
        client_id = request.POST.get('client_id', None)
        project_assign = request.POST.get('project_assign', None)
        local_timezone = request.POST.get('timezone', None)

        submit_success = ''

        if client_id and employee_id and project_assign:
            user_evaluation = UserEvaluation.objects.create(
                employee_id=employee_id,
                client_id=client_id,
                hr_admin=request.user,
                project_assign=project_assign
            )
            
            local_time_convert = timezone.localtime(user_evaluation.searchable_assigned_date, pytz.timezone(local_timezone))
            user_evaluation.searchable_assigned_date = local_time_convert.strftime('%b. %e, %Y, %I:%M %p')
            user_evaluation.save()

            employee = Employee.objects.get(pk=employee_id)
            employee.current_user_evaluation = user_evaluation

            client = Client.objects.get(pk=client_id)

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
            
            submit_success = 'success'
        
        return self.render(
            request,
            context_overrides={
                'notification_url' : HRIndexPage.objects.live().first().url ,
                'employee_list_index' : EmployeeListPage.objects.live().first(),
                'client_list_index' : ClientListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': ReportsHR.objects.live().first(),
                'submit_success': submit_success
            }
        )

    @route(r'^(\d+)/$')
    def client_list(self, request, employee_id):
        

        return self.render(
            request,
            context_overrides={
                'notification_url' : HRIndexPage.objects.live().first().url ,
                'employee_list_index' : EmployeeListPage.objects.live().first(),
                'client_list_index' : ClientListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'employee': Employee.objects.get(pk=employee_id),
                'reports_index': ReportsHR.objects.live().first(),
            },
            template='hr/assign_client.html'
        )
    
    @route(r'^(\d+)/search/clients/$')
    def client_search(self, request, id):

        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        sort = request.GET.get('sort', '')

        employee = Employee.objects.get(pk=id)

        if name or address or contact_number:
            if sort:
                clients = Client.objects.filter(company__icontains=name, address__icontains=address, contact_number__icontains=contact_number).order_by(sort)
            else:
                clients = Client.objects.filter(company__icontains=name, address__icontains=address, contact_number__icontains=contact_number)
        else:
            if sort:
                clients = Client.objects.all().order_by(sort)
            else:
                clients = Client.objects.all()

        clients = self.paginate_data(clients, page)
        max_pages = clients.paginator.num_pages
        starting_point = clients.number
        next_number = 1
        previous_number = 1

        if clients.has_next():
            next_number = clients.next_page_number()
        
        if clients.has_previous():
            previous_number = clients.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 


        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'hr/assign_search_client.html',
                        {
                            'clients' : clients,
                            'employee': employee
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': clients,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': clients.number,
                },
            )

    @route(r'^search/employees/$')
    def employee_search(self, request):
        page = request.GET.get('page', 1)

        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        contact_number = request.GET.get('contact_number', '')
        position = request.GET.get('position', '')
        sort = request.GET.get('sort', '')

        if name or address or contact_number or sort or position:
            employees = None

            if name:
                name = name.split()
                qset1 =  reduce(operator.__or__, [Q(first_name__icontains=query) | Q(last_name__icontains=query) for query in name])
                employees = Employee.objects.filter(qset1).distinct()
                if sort:
                    employees = employees.filter(
                        address__icontains=address, 
                        contact_number__icontains=contact_number, 
                        position__icontains=position
                    ).order_by(sort)
                else:
                    employees = employees.filter(
                        address__icontains=address, 
                        contact_number__icontains=contact_number, 
                        position__icontains=position
                    )
                employees = employees.filter(Q(current_user_evaluation=None) | Q(current_user_evaluation__performance__gt=0 ))
                
            else:
                if sort:
                    employees = Employee.objects.filter(
                        address__icontains=address,
                        contact_number__icontains=contact_number,
                        position__icontains=position
                    ).order_by(sort)
                else:
                    employees = Employee.objects.filter(
                        address__icontains=address, 
                        contact_number__icontains=contact_number, 
                        position__icontains=position
                    )
                
                employees = employees.filter(Q(current_user_evaluation=None) | Q(current_user_evaluation__performance__gt=0 ))
        else:
            employees = Employee.objects.filter( Q(current_user_evaluation=None) )

        

        employees = self.paginate_data(employees, page)
        max_pages = employees.paginator.num_pages
        starting_point = employees.number
        next_number = 1
        previous_number = 1

        if employees.has_next():
            next_number = employees.next_page_number()
        
        if employees.has_previous():
            previous_number = employees.previous_page_number()

        if max_pages > 3 :
            max_pages = 4

        if starting_point % 3 == 0:
            starting_point = starting_point - 2
        elif (starting_point - 1) % 3  != 0:
            starting_point = starting_point - 1 


        return JsonResponse(
                data={
                    'html' : render_to_string(
                        'hr/assign_search_employee.html',
                        {
                            'employee_details_index': EmployeeDetailsPage.objects.live().first().url,
                            'employees' : employees,
                        }
                    ),
                    'pages_indicator': render_to_string(
                        'includes/page_indicator.html',
                        {
                            'pages': employees,
                            'xrange': range(starting_point, starting_point + max_pages)
                        }
                    ),
                    'next_number': next_number,
                    'previous_number': previous_number,
                    'current_number': employees.number,
                },
            )

class ReportsHR(RoutablePageMixin, Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']

    def paginate_data(self, data, current_page):
        paginator = Paginator(data, 7)

        try:
            data = paginator.page(current_page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        return data
    
    @route(r'^$') 
    def default_route(self, request):
        
        return self.render(
            request,
            context_overrides={
                'user_model': request.user.hradmin,
                'notification_url' : HRIndexPage.objects.live().first().url ,
                'employee_list_index' : EmployeeListPage.objects.live().first(),
                'client_list_index' : ClientListPage.objects.live().first(),
                'assign_employee_index': AssignEmployee.objects.live().first(),
                'reports_index': self,
            })
    
    @route(r'^(\d+)/$')
    def details_user_route(self, request, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        employee = user_evaluation.employee
        categories = EvaluationCategories.objects.all()
        max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        category_percentages = []
        overall_performance = 0


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
            
            overall_performance = overall_performance + percentage
            
            category_percentages.append([category,percentage])

        if overall_performance != 0:
            overall_performance = overall_performance / len(categories)
            
        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()
        assign_employee_index = AssignEmployee.objects.live().first()
        
        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'user_model': request.user.hradmin ,
            'category_percentages': category_percentages,
            'current_menu':'reports',
            'assign_employee_index': assign_employee_index,
            'employee_list_index': employee_list_index,
            'client_list_index': client_list_index,
            'notification_url': HRIndexPage.objects.live().first().url,
            'reports_index': self,
            'max_rate' : max_rate,
            'overall_performance': overall_performance,
            'employee': employee,
            },
            template='hr/employee_details_page.html'
            
        )

    @route(r'^(\d+)/evaluation/$')
    def client_evaluation_details(self, request, user_evaluation_id):
        user_evaluation = UserEvaluation.objects.get(pk=user_evaluation_id)
        evaluation_max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
        legend_evaluation = EvaluationPage.objects.live().first().legend_evaluation

        
        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()
        assign_employee_index = AssignEmployee.objects.live().first()

        return self.render(
            request,
            context_overrides={
                'user_evaluation': user_evaluation,
                'evaluation_categories': EvaluationCategories.objects.all(),
                'disabled' : True,
                'user_model' : request.user.hradmin,
                'employee_model': user_evaluation.client,
                'self': {'evaluation_max_rate': evaluation_max_rate, 'legend_evaluation': legend_evaluation},
                'current_menu':'reports',
                'assign_employee_index': assign_employee_index,
                'employee_list_index': employee_list_index,
                'client_list_index': client_list_index,
                'notification_url': HRIndexPage.objects.live().first().url,
                'reports_index': self,
            },
            template="base/evaluation_page.html",
        )

    @route(r'^search/evaluations/$')
    def evaluation_search(self, request):

        page = request.GET.get('page', 1)

        employee = request.GET.get('employee', '')
        client = request.GET.get('client', '')
        project_assign = request.GET.get('project_assign', '')
        performance = request.GET.get('performance', '')
        date = request.GET.get('date', '')

        sort = request.GET.get('sort', '')
        timezone = request.GET.get('timezone', '')

        user_evaluations = None

        if employee or client or project_assign or date or performance or sort:

            if employee:
                employee_name = employee.split()
                qset1 =  reduce(operator.__or__, [Q(employee__first_name__icontains=query) | Q(employee__last_name__icontains=query) for query in employee_name])
                
                user_evaluations = UserEvaluation.objects.filter(qset1).distinct()

                if sort:
                    user_evaluations = user_evaluations.filter(client__company__icontains=client, project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date).order_by(sort)
                else:
                    user_evaluations = user_evaluations.filter(client__company__icontains=client, project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date)
            else:
                if sort:
                    user_evaluations = UserEvaluation.objects.filter(client__company__icontains=client, project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date).order_by(sort)
                else:
                    user_evaluations = UserEvaluation.objects.filter(client__company__icontains=client, project_assign__icontains=project_assign, performance__icontains=performance, searchable_assigned_date__icontains=date)
            
        else:
            if sort:
                user_evaluations = UserEvaluation.objects.all().order_by(sort)
            else:
                user_evaluations = UserEvaluation.objects.all().order_by('-submit_date','assigned_date')
        

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
                        'hr/search_reports.html',
                        {
                            'user_evaluations' : user_evaluations,
                            'timezone': timezone,
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

    def get_context(self, request):
        context = super(HRIndexPage, self).get_context(request)

        employee_list_index = EmployeeListPage.objects.live().first()
        client_list_index = ClientListPage.objects.live().first()
        assign_employee_index = AssignEmployee.objects.live().first()
        reports_index = ReportsHR.objects.live().first()
 
        context['employee_list_index'] = employee_list_index
        context['client_list_index'] = client_list_index
        context['assign_employee_index'] = assign_employee_index
        context['reports_index'] = reports_index

        context['client_count'] = len(Client.objects.all())
        context['employee_count'] = len(Employee.objects.all())

        return context

