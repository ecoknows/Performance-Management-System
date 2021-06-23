from django.db import models
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from wagtail.contrib.routable_page.models import route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system.base.models import BaseAbstractPage
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource

class HRIndexPage(BaseAbstractPage):
    max_count = 1

    parent_page_types = ['base.BaseIndexPage']
    
class ClientListPage(Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']

    def get_clients(self):
        return Client.objects.all()

    def get_context(self, request):
        context = super(ClientListPage, self).get_context(request)

        context['clients'] = self.get_clients()
        return context

class EmployeeListPage(Page):
    max_count = 1
    parent_page_types = ['HRIndexPage']
    
    def get_employees(self):
        return Employee.objects.all()

    def get_context(self, request):
        context = super(EmployeeListPage, self).get_context(request)

        context['employees'] = self.get_employees()
        return context

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

    
    parent_page_types = ['ClientListPage']


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