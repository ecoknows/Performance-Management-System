
from django.contrib.auth.models import Group
from django.utils import timezone

from wagtail.contrib.modeladmin.views import CreateView

from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource

class EmployeeCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()

        id = str(IntegerResource.EMPLOYEE_INDEX + instance.pk)
        year_now = str(timezone.now().year - 2000) 
        username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
        
        user = User.objects.create_user(
            username=username,
            first_name= instance.first_name,
            last_name=instance.last_name,
            is_employee=True,
            email=instance.first_name + '.' + instance.last_name + StringResource.COMPANTY_EMAIL_SUFFIX,
        )

        instance.user = user
        user.set_password(instance.last_name.upper())
        user.save()
        
        group = Group.objects.get(name=StringResource.EMPLOYEE)
        
        group.user_set.add(user)

        return super().form_valid(form)
