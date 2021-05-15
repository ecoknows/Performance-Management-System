from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable

from wagtail.core import blocks
from modelcluster.models import ClusterableModel
from django.http import HttpResponseRedirect
from performance_management_system import StringResource, IntegerResource
from django.utils import timezone


        
        

class EvaluationSubCategories(Orderable):
    model = ParentalKey("home.EvaluationCategories",
                        related_name="evaluation_sub_categories")
    sub_category = models.CharField(max_length=255, blank=True)
    rate_maximum = models.IntegerField(default=1)

    panels = [
        FieldPanel("sub_category"),
        FieldPanel("rate_maximum"),
    ]


class EvaluationCategories(ClusterableModel, Orderable):
    model = ParentalKey("home.Evaluations",
                        related_name="evaluation_categories")
    category = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("category"),
        MultiFieldPanel([
            InlinePanel('evaluation_sub_categories',
                        label='Sub Category', min_num=0, max_num=4)
        ], heading='Form')
    ]


class Evaluations(Page):

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('evaluation_categories',
                        label='Category', min_num=0, max_num=4)
        ], heading='Evaluation Form')
    ]


class Client(models.Model):
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)

    panels = [
        FieldPanel('company'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
    ]

    def client_id(self):
        id = str(IntegerResource.USERNAME_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    def __str__(self):
        return self.company


class Employee(models.Model):
    first_name = models.CharField(max_length=25, null=True)
    middle_initial = models.CharField(max_length=1,null=True)
    last_name = models.CharField(max_length=25,null=True)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    birth_day = models.DateField()
    position = models.CharField(max_length=255)
    

    panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('middle_initial'),
            FieldPanel('last_name'),    
        ], heading='Employee Complete Name'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
        FieldPanel('birth_day'),
        FieldPanel('position'),
    ]
    
    def employee_id(self):
        id = str(IntegerResource.USERNAME_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    def employee(self):
        return self.last_name + ', ' + self.first_name + ' ' +  self.middle_initial + '.' 

    def __str__(self):
        return self.first_name


class Question(models.Model):
    company_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('company_name'),
    ]

    def __str__(self):
        return self.company_name


class Assigns(models.Model):
    client = models.ForeignKey(
        'home.Client', null=True, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        'home.Employee', null=True, on_delete=models.CASCADE)

    panels = [
        FieldPanel('client'),
        FieldPanel('employee'),
    ]
    
    
    def __str__(self):
        return self.client.company
    


class HomePage(Page):
    
    def serve(self, request):
        if request.user.is_authenticated == False:
            return HttpResponseRedirect('/login/')
        return super().serve(request)
    
    def get_context(self, request):
        context = super().get_context(request)
        
        context['group'] = str(request.user.groups.all()[0])
        context['assigns'] = Assigns.objects.filter(client__company=request.user.first_name)
        
        return context;