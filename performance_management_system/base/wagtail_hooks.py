

from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)


from performance_management_system.client.models import Client
from performance_management_system.client.views import ClientCreateView

from performance_management_system.employee.models import Employee
from performance_management_system.employee.views import EmployeeCreateView

from performance_management_system.hr.models import HrAdmin
from performance_management_system.hr.views import HRAdminCreateView

from performance_management_system.base.models import UserEvaluation
     

class EmployeesInfo(ModelAdmin):
    model = Employee
    create_view_class = EmployeeCreateView
    menu_label = 'Employees'
    menu_icon = 'group'
    list_display = ('employee','display_image')
    search_fields = ('employee',)
    
modeladmin_register(EmployeesInfo)

class HRAdminInfo(ModelAdmin):
    model = HrAdmin
    create_view_class = HRAdminCreateView
    menu_label = 'HR Admin'
    menu_icon = 'group'
    list_display = ('hr_admin','hr_id','display_image')
    search_fields = ('hr_admin',)
    
modeladmin_register(HRAdminInfo)


class ClientsInfo(ModelAdmin):
    model = Client
    create_view_class = ClientCreateView
    menu_label = 'Clients'
    menu_icon = 'group'
    list_display = ('company','display_image')
    
modeladmin_register(ClientsInfo)

class Evaluation(ModelAdmin):
    model = UserEvaluation
    menu_label = 'Evaluation'
    menu_icon = 'doc-full'
    list_display = ('employee','client', 'evaluated',)
    inspect_view_enabled = True
    inspect_template_name = 'modeladmin/inspect_evaluation.html'
    
modeladmin_register(Evaluation)

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

