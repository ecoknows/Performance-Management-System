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


class HomePage(Page):
    pass

class EvaluationSubCategories(Orderable):
    model = ParentalKey("home.EvaluationCategories", related_name="evaluation_sub_categories")
    sub_category = models.CharField(max_length=255, blank=True)
    rate_maximum = models.IntegerField(default=1)

    panels = [
            FieldPanel("sub_category"),
            FieldPanel("rate_maximum"),
    ]

class EvaluationCategories(ClusterableModel,Orderable):
    model = ParentalKey("home.Evaluations", related_name="evaluation_categories")
    category = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("category"),
        MultiFieldPanel([
            InlinePanel('evaluation_sub_categories',label='Sub Category', min_num=0, max_num=4)
        ], heading = 'Form')
    ]

class Evaluations(Page):
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('evaluation_categories', label='Category',min_num=0, max_num=4)
        ], heading = 'Evaluation Form')
    ]
    pass

class Client(models.Model):
    client_no = models.CharField(max_length=255)
    company = models.ForeignKey('home.Companies',on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)


    panels = [
        FieldPanel('client_no'),
        FieldPanel('company'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
        FieldPanel('client_name'),
    ]



    def __str__(self):
        return self.client_name

class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    birth_day = models.DateField()
    position = models.CharField(max_length=255)

    panels = [
        FieldPanel('employee_name'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
        FieldPanel('birth_day'),
        FieldPanel('position'),
    ]

    def __str__(self):
        return self.employee_name

class Companies(models.Model):
    company_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('company_name'),
    ]

    def __str__(self):
        return self.company_name

class Question(models.Model):
    company_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('company_name'),
    ]

    def __str__(self):
        return self.company_name

class Assigns(models.Model):
    client = models.ForeignKey('home.Client',null=True,on_delete=models.CASCADE)
    employee = models.ForeignKey('home.Employee',null=True,on_delete=models.CASCADE)

    panels = [
        FieldPanel('client'),
        FieldPanel('employee'),
    ]

