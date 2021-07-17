from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from wagtail.core.models import Page

from wagtail.admin.edit_handlers import (
    FieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from performance_management_system import IntegerResource, StringResource, IS_EVALUATED, LIST_MENU
from performance_management_system.users.models import User
from performance_management_system.employee.models import Employee


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    profile_pic = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    company = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    contact_number = models.CharField(max_length=255, null=True)
    
    status = models.CharField(
        max_length=255,
        choices=IS_EVALUATED,
        default='none'
    )
    

    panels = [
        ImageChooserPanel('profile_pic'),
        FieldPanel('company'),
        FieldPanel('address'),
        FieldPanel('contact_number'),
    ]
    
    @property
    def client_id(self):
        id = str(IntegerResource.CLIENT_INDEX + self.pk)
        year_now = str(timezone.now().year - 2000) 
        return StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id;
    
    @property
    def display_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.profile_pic.get_rendition('fill-200x100').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''

    def __str__(self):
        return self.company
    
    def delete(self):
        if self.user:
            self.user.delete()
        super().delete()        
  

class ClientIndexPage(Page):
    max_count = 1

    def get_menu_list(self):
        return LIST_MENU

    def get_assign_employee(self, request, context):
        from performance_management_system.base.models import UserEvaluation
        filter_query = request.GET.get('filter', None)
        
        if filter_query:
            if filter_query == 'evaluated':
                context['filter'] = 'Evaluated'
                return UserEvaluation.objects.exclude(percentage=0).filter(
                    client=request.user.client
                )
            elif filter_query == 'on evaluation':
                context['filter'] = 'On Evaluation'
                return UserEvaluation.objects.filter(
                    percentage=0,
                    client=request.user.client
                )

        return UserEvaluation.objects.filter(client=request.user.client)
        
    def get_context(self, request):
        context = super(ClientIndexPage, self).get_context(request)

        context['user_evaluations'] = self.get_assign_employee(request, context)
        context['menu_lists'] = self.get_menu_list()

        return context