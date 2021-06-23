from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from wagtail.core.models import Page

from wagtail.admin.edit_handlers import (
    FieldPanel,
)

from performance_management_system import IntegerResource, StringResource
from performance_management_system.users.models import User

class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    company = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    contact_number = models.CharField(max_length=255, null=True)

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
        
        user = User.objects.create_user(username='temp')
        self.user = user
        
        super().save()
        
        
        
        id = str(IntegerResource.CLIENT_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
        
        user.set_password(self.company.upper())
        user.username = username
        user.email = self.company + StringResource.COMPANTY_EMAIL_SUFFIX,
        user.save()
        
        group = Group.objects.get(name=StringResource.CLIENT)
        
        group.user_set.add(user)


class ClientIndexPage(Page):
    max_count = 1