from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


class HomePage(Page):
    pass


class Client(models.Model):
    client_no = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)

    panels = [
        FieldPanel('client_no'),
        FieldPanel('company_name'),
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


