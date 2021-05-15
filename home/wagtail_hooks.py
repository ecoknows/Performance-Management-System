

from wagtail.core import hooks
from django.contrib.auth.models import User, Group
from performance_management_system import StringResource, IntegerResource

from wagtail.contrib.modeladmin.views import CreateView
from django.utils import timezone

from .models import (
    Client,
    Employee,
    Assigns
)
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
class CustomView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()
        id = str(IntegerResource.USERNAME_INDEX + instance.pk)
        year_now = str(timezone.now().year - 2000) 
        username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
        
        if self.model_admin.group_name == StringResource.EMPLOYEE:
            user = User.objects.create_user(
                username=username,
                first_name= instance.first_name or instance.company,
                last_name= instance.last_name,
                password=instance.last_name.upper() + id,
                email=instance.first_name + '.' + instance.last_name + StringResource.COMPANTY_EMAIL_SUFFIX,
            )
        else:
            user = User.objects.create_user(
                username=username,
                first_name=instance.company,
                password=instance.company.upper() + id,
                email=instance.company + StringResource.COMPANTY_EMAIL_SUFFIX,
            )
            
        
        group = Group.objects.get(name=self.model_admin.group_name)
        
        group.user_set.add(user)
        
        return super().form_valid(form)        

class EmployeesInfo(ModelAdmin):
    model = Employee
    create_view_class = CustomView
    group_name = StringResource.EMPLOYEE
    menu_label = 'Employees'
    menu_icon = 'group'
    list_display = ('employee_id','employee','address','contact_number', 'birth_day', 'position')
    search_fields = ('employee_id','employee','address','contact_number', 'birth_day', 'position')
    
    


modeladmin_register(EmployeesInfo)


class ClientsInfo(ModelAdmin):
    model = Client
    create_view_class = CustomView
    group_name = StringResource.CLIENT
    menu_label = 'Clients'
    menu_icon = 'group'
    list_display = ('client_id','company', 'address', 'contact_number')
    # list_filter = ('company',)
    # search_fields = ('company', 'address', 'contact_number')


modeladmin_register(ClientsInfo)

@hooks.register("construct_main_menu")
def hide_documents(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "documents"]
    
@hooks.register("construct_main_menu")
def hide_documents(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "images"]


@hooks.register("construct_main_menu")
def hide_workflows(request, menu_items):
    if request.user.is_superuser is False:
        menu_items[:] = [item for item in menu_items if item.name != "reports"]

class AssignsInfo(ModelAdmin):
    model = Assigns
    menu_label = 'Assign'
    menu_icon = 'list-ul'

    list_display = ('client', 'employee',)
    list_filter = ('client',)
    search_fields = ('client', 'employee',)

modeladmin_register(AssignsInfo)
