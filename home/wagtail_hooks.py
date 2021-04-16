from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
	ModelAdminGroup,
	modeladmin_register
)
from .models import (
	Client,
	Employee
)


class ClientsInfo(ModelAdmin):
	model = Client
	menu_label = 'Clients'
	menu_icon = 'group'
	list_display = ('client_no', 'company_name', 'address', 'contact_number', 'client_name')
	list_filter = ('company_name',)
	search_fields = ('client_no', 'company_name', 'address', 'contact_number', 'client_name')

class EmployeesInfo(ModelAdmin):
	model = Employee
	menu_label = 'Employees'
	menu_icon = 'group'
	list_display = ('employee_name', 'address', 'contact_number', 'birth_day', 'position')
	list_filter = ('position',)
	search_fields = ('employee_name', 'address', 'contact_number', 'birth_day', 'position')

class DataAdminGroup(ModelAdminGroup):
	menu_label = 'Datas'
	menu_order = 100
	items = (ClientsInfo,EmployeesInfo)

modeladmin_register(DataAdminGroup)