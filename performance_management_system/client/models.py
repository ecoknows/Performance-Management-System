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
    
    def save(self):
        super().save()
        if self.pk is None:
            from performance_management_system.users.models import User
            
            id = str(IntegerResource.CLIENT_INDEX + self.pk)
            year_now = str(timezone.now().year - 2000) 
            username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
            
            user = User.objects.create_user(
                username=username,
                first_name=self.company,
                password=self.company.upper() + id,
                client=self,
                email=self.company + StringResource.COMPANTY_EMAIL_SUFFIX,
            )
                
            
            group = Group.objects.get(name=StringResource.CLIENT)
            
            group.user_set.add(user)
        


class ClientIndexPage(Page):
    max_count = 1