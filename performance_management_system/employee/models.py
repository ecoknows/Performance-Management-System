
from django.db import models
from django.utils import timezone
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
)

from performance_management_system import IntegerResource, StringResource



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
    
    @property
    def employee_id(self):
        id = str(IntegerResource.EMPLOYEE_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    @property
    def employee(self):
        return self.last_name + ', ' + self.first_name + ' ' +  self.middle_initial + '.' 

    def __str__(self):
        return self.employee
            
    
class EmployeeIndexPage(Page):
    max_count = 1