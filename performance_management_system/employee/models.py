
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
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
    evaluated = models.BooleanField(default=False)
    

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
        FieldPanel('evaluated'),
    ]
    
    @property
    def assigned_client(self):
        return self.client.all().first()
    
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
    
    def save(self):
        
        super().save()
        if self.pk is None:
            from performance_management_system.users.models import User
            id = str(IntegerResource.EMPLOYEE_INDEX + self.pk)
            year_now = str(timezone.now().year - 2000) 
            username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
            
            user = User.objects.create_user(
                username=username,
                first_name= self.first_name or self.company,
                last_name= self.last_name,
                password=self.last_name.upper() + id,
                employee=self,
                email=self.first_name + '.' + self.last_name + StringResource.COMPANTY_EMAIL_SUFFIX,
            )
            
            group = Group.objects.get(name=StringResource.EMPLOYEE)
            
            group.user_set.add(user)
            
    
class EmployeeIndexPage(Page):
    max_count = 1