
from django.contrib.auth.models import Group
from django.utils import timezone

from wagtail.contrib.modeladmin.views import CreateView

from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource

class ClientCreateView(CreateView):
    
    def form_valid(self, form):

        # id = str(IntegerResource.CLIENT_INDEX + instance.pk)
        # year_now = str(timezone.now().year - 2000) 
        # username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
        
        # user = User.objects.create_user(
        #     username=username,
        #     password=instance.company.upper(),
        #     email=instance.company + StringResource.COMPANTY_EMAIL_SUFFIX,
        # )
            
        # instance.user = user
        
        # group = Group.objects.get(name=StringResource.CLIENT)
        
        # group.user_set.add(user)


        return super().form_valid(form)
