from django.db import models
from django.contrib.auth.models import AbstractUser
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client

class User(AbstractUser):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )