from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    TabbedInterface,

)
from wagtail.core.models import Page


class HomePage(Page):
    pass


class LoginPage(Page):
    max_count = 1


class Client(models.Model):
    client_no = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True)
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
