from datetime import timedelta
from django.utils import timezone
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from performance_management_system import GRADIENT_BG
from performance_management_system.base.models import EvaluationTask

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='to_str') 
def to_str(number):
    return str(number)

@register.simple_tag
def get_rate_assign(rate, user_evaluation):
    rate_assigns = user_evaluation.evaluation_rates_assign.all()
    for rate_assign in rate_assigns:
        if rate_assign.evaluation_rate == rate:
            rate.rate = rate_assign.rate
            break

    return ''

@register.simple_tag
def get_task(user_evaluation, category):
    try:
        if user_evaluation.submit_date:
            task = user_evaluation.evaluation_task.get(category=category)
            return task.text
    except EvaluationTask.DoesNotExist:
        return ''
    
    return ''


@register.filter(name='gradient_bg')
def gradient_bg(id):
    return 'background-image: linear-gradient('+GRADIENT_BG[id-1][0]+','+ GRADIENT_BG[id-1][1]+')'

@register.filter(name="for_evaluation_filter")
def for_evaluation_filter(user_evaluation):
    
    if user_evaluation == None:
        return 'none'
        
    date = user_evaluation.assigned_date

    ending_date = date + timedelta(weeks=1)

    result = ending_date

    return result


@register.simple_tag
def check_status(user_evaluation):
    
    if user_evaluation == None:
        return 'none'

    if user_evaluation.submit_date :
        return 'done-evaluating'
    else:
        return 'for-evaluation'