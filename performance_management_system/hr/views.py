
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

    employee_evaluations = UserEvaluation.objects.exclude(percentage=0).filter(employee_id = employee_id)
    max_rate = EvaluationPage.objects.live().first().evaluation_max_rate
    
    page = request.GET.get('page', 1)
    max_page = request.GET.get('max_page', 1)
    is_2x2 = request.GET.get('2x2', False)

    

    label = []
    data = []
    table = []

    # evaluation_rate_assigns = EvaluationRateAssign.objects.filter(evaluation_rate__evaluation_categories_id=category_id, user_evaluation__employee_id=employee_id).order_by('user_evaluation__client')
    
    # summation = 0
    # n = 0
    # client_name = None

    # for evaluation_rate_assign in evaluation_rate_assigns:
    #     summation = summation + evaluation_rate_assign.rate 
    #     current_client_name = evaluation_rate_assign.user_evaluation.client.company
    #     n = n + 1
    #     if client_name != current_client_name:
    #         client_name = current_client_name
    #         print(summation)
    #         if n != 0:
    #             percentage = math.ceil((summation / 15) * 100)
    #             label.append(client_name)
    #             data.append(percentage)
    #             table.append([client_name, percentage])
    #             summation = 0
    #             n = 0


    ## DEYM

    for employee_evaluation in employee_evaluations:
        client_name = employee_evaluation.client.company


        evaluations = employee_evaluation.evaluation_rates_assign.filter(
            evaluation_rate__evaluation_categories_id=category_id
        )


        n = len(evaluations)
        summation = 0
        


        if n != 0:
            for evaluation in evaluations:
                summation = summation + evaluation.rate
            percentage = math.ceil(((summation/n) / max_rate) * 100)
            label.append(client_name)
            data.append(percentage)
            table.append([client_name, percentage])

    paginator = Paginator(data, max_page)
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        
    paginator = Paginator(label, max_page)
    
    try:
        label = paginator.page(page).object_list
    except PageNotAnInteger:
        label = paginator.page(1).object_list
    except EmptyPage:
        label = paginator.page(paginator.num_pages).object_list

    
    paginator = Paginator(table, max_page)
    
    try:
        table = paginator.page(page).object_list
    except PageNotAnInteger:
        table = paginator.page(1).object_list
    except EmptyPage:
        table = paginator.page(paginator.num_pages).object_list
    

        
    return JsonResponse(data={
        'labels': label,
        'data': data.object_list,
        'html_chart' : render_to_string('includes/chart_table.html', {'tables': table, 'is_2x2': is_2x2}),
        'has_previous' : data.has_previous(),
        'has_next' : data.has_next()
    })

def get_recent(request):
    recent_evaluations = UserEvaluation.objects.exclude(percentage=0).order_by('-submit_date')
            
    page = request.GET.get('page', 1)

    paginator = Paginator(recent_evaluations, 8)

    
    try:
        recent_evaluations = paginator.page(page)
    except PageNotAnInteger:
        recent_evaluations = paginator.page(1)
    except EmptyPage:
        recent_evaluations = paginator.page(paginator.num_pages)
    
    return JsonResponse(data={
        'has_next': recent_evaluations.has_next(),
        'has_previous': recent_evaluations.has_previous(),
        'html' : render_to_string('hr/recent_evaluated_page.html', {
            'recent_evaluations': recent_evaluations,
            'employee_details_index' : EmployeeDetailsPage.objects.live().first()
        }),
    })