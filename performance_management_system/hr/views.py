
from django.contrib.auth.models import Group
from django.utils import timezone

from wagtail.contrib.modeladmin.views import CreateView

from performance_management_system.base.models import EvaluationRateAssign, UserEvaluation, EvaluationCategories, EvaluationPage
from performance_management_system.hr.models import EmployeeDetailsPage
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import math, re

class HRAdminCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()

        id = str(IntegerResource.HR_INDEX + instance.pk)
        year_now = str(timezone.now().year - 2000) 
        
        username = re.sub(r"[^\w\s]", '', instance.last_name)
        username = re.sub(r"\s+", '-', username)
         
        username = 'HR-'+username.upper() + '-' +  year_now + '-' + id
        
        
        
        user = User.objects.create_user(
            username=username,
            first_name= instance.first_name,
            last_name=instance.last_name,
            is_hr=True,
            email=instance.first_name + '.' + instance.last_name + StringResource.COMPANTY_EMAIL_SUFFIX,
        )

        instance.user = user
        password = re.sub(r"\s+", '', instance.last_name)
        user.set_password(password.upper())
        user.save()
        
        group = Group.objects.get(name=StringResource.HR_ADMIN)
        
        group.user_set.add(user)

        return super().form_valid(form)
