
from django.contrib.auth.models import Group
from django.utils import timezone

from wagtail.contrib.modeladmin.views import CreateView

from performance_management_system.base.models import UserEvaluation, EvaluationCategories, EvaluationPage
from performance_management_system.users.models import User
from performance_management_system import IntegerResource, StringResource

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import math

class HRAdminCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()

        id = str(IntegerResource.HR_INDEX + instance.pk)
        year_now = str(timezone.now().year - 2000) 
        username = StringResource.COMPANY_PREFIX_TAG + '-' +  year_now + '-' + id
        
        user = User.objects.create_user(
            username=username,
            first_name= instance.first_name,
            last_name=instance.last_name,
            is_hr=True,
            email=instance.first_name + '.' + instance.last_name + StringResource.COMPANTY_EMAIL_SUFFIX,
        )

        instance.user = user
        user.set_password(instance.last_name.upper())
        user.save()
        
        group = Group.objects.get(name=StringResource.HR_ADMIN)
        
        group.user_set.add(user)

        return super().form_valid(form)

def data_chart(request, category_id, employee_id):

    employee_evaluations = UserEvaluation.objects.filter(employee_id = employee_id, evaluated = True)
    max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
    
    page = request.GET.get('page', 1)
    max_page = request.GET.get('max_page', 1)
    is_2x2 = request.GET.get('2x2', False)

    paginator = Paginator(employee_evaluations, max_page)
    

    label = []
    data = []
    table = []

    try:
        employee_evaluations = paginator.page(page)
    except PageNotAnInteger:
        employee_evaluations = paginator.page(1)
    except EmptyPage:
        employee_evaluations = paginator.page(paginator.num_pages)

    for employee_evaluation in employee_evaluations:
        client_name = employee_evaluation.client.company


        evaluations = employee_evaluation.evaluation_rates_assign.filter(
            evaluation_rate__evaluation_categories_id=category_id
        )

        n = len(evaluations)
        summation = 0

        for evaluation in evaluations:
            summation = summation + evaluation.rate

        percentage = math.ceil(((summation/n) / max_rate) * 100)
        label.append(client_name)
        data.append(percentage)
        table.append([client_name, percentage])
    

        
    return JsonResponse(data={
        'labels': label,
        'data': data,
        'html_chart' : render_to_string('includes/chart_table.html', {'tables': table, 'is_2x2': is_2x2}),
        'has_previous' : employee_evaluations.has_previous(),
        'has_next' : employee_evaluations.has_next()
    })