from django.db import models
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render

from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page

from performance_management_system.base.models import BaseAbstractPage
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client

class HRIndexPage(BaseAbstractPage):
    max_count = 1 
    
    @route(r'^$') 
    def default_serve(self, request):
        persons = Employee.objects.all()
        if "group" in request.GET:
            
            group = request.GET.get('group', None)
            
            if group == 'Client':
                persons = Client.objects.all()
                return TemplateResponse(
                    request, 
                    'hr/person_card.html',{
                        'group' : group,
                        'persons': persons,
                        'details_url' : 'client-details-page'
                    }
                )
            elif group == 'Employee':
                persons = Employee.objects.all()
                return TemplateResponse(
                    request, 
                    'hr/person_card.html',{
                        'group' : group,
                        'persons': persons,
                        'details_url' : 'employee-details-page'
                    }
                )
                
        
        return self.render(
            request, 
            context_overrides={
                'group' : 'Employee',
                'persons': persons,
                'details_url' : 'employee-details-page'
            }
        )
        

class ClientDetailsPage(Page):
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


class EmployeeDetailsPage(Page):
    max_count = 1
    
    def serve(self, request):
        
        if "query" in request.GET:
            try:
                return render(request, self.template,{
                    'employee': Employee.objects.get(pk=request.GET['query'])
                })
            except Employee.DoesNotExist:
                return redirect('/')
            
        
        return super().serve(request)
    
    
        
