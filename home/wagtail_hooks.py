from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from .models import (
    Client,
    Employee,
    Assigns
)
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from django.urls import reverse
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render


class EmployeesInfo(ModelAdmin):
    model = Employee
    menu_label = 'Employees'
    menu_icon = 'group'
    list_display = ('employee_name', 'address',
                    'contact_number', 'birth_day', 'position')
    list_filter = ('position',)
    search_fields = ('employee_name', 'address',
                     'contact_number', 'birth_day', 'position')


modeladmin_register(EmployeesInfo)


class ClientsInfo(ModelAdmin):
    model = Client
    menu_label = 'Clients'
    menu_icon = 'group'
    list_display = ('client_no', 'company', 'address',
                    'contact_number', 'client_name')
    list_filter = ('company',)
    search_fields = ('client_no', 'company', 'address',
                     'contact_number', 'client_name')


modeladmin_register(ClientsInfo)


class AssignsInfo(ModelAdmin):
    model = Assigns
    menu_label = 'Assigns'
    menu_icon = 'list-ul'


modeladmin_register(AssignsInfo)
