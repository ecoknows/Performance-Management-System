from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from wagtail.core.models import Page

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system import IntegerResource, StringResource
from performance_management_system.employee.models import Employee

class Client(models.Model):
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)

    panels = [
        FieldPanel('company'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
    ]
    
    @property
    def client_id(self):
        id = str(IntegerResource.CLIENT_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    def __str__(self):
        return self.company


class ClientIndexPage(Page):
    max_count = 1