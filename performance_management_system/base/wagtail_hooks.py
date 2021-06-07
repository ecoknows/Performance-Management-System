

from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)


from performance_management_system.client.models import Client
from performance_management_system.employee.models import Employee
from performance_management_system.base.models import UserEvaluation
     

class EmployeesInfo(ModelAdmin):
    model = Employee
    menu_label = 'Employees'
    menu_icon = 'group'
    list_display = ('employee',)
    search_fields = ('employee',)
    
modeladmin_register(EmployeesInfo)


class ClientsInfo(ModelAdmin):
    model = Client
    menu_label = 'Clients'
    menu_icon = 'group'
    list_display = ('company',)
    
modeladmin_register(ClientsInfo)

class Evaluation(ModelAdmin):
    model = UserEvaluation
    menu_label = 'Evaluation'
    menu_icon = 'doc-full'
    list_display = ('employee','client', 'evaluated')
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

