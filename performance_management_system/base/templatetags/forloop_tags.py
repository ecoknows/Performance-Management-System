from datetime import date, time, timedelta
from django.utils import timezone
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from performance_management_system import GRADIENT_BG
from performance_management_system.base.models import CalendarOrderable, EvaluationTask

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
    # date = timezone.now()

    rules = CalendarOrderable.objects.all()

    for rule in rules:

        if rule.calendar == 'day':
            ending_date = date + timedelta(days=rule.count)
        if rule.calendar == 'week':
            ending_date = date + timedelta(days=rule.count * 7)
        if rule.calendar == 'month':
            ending_date = date + timedelta(days=rule.count * 30)
        if rule.calendar == 'year':
            ending_date = date + timedelta(days=rule.count * 365)

        if ending_date > timezone.now():
            return ending_date

    return None

@register.simple_tag
def check_if_time_exceed(user_evaluation):
    
    if user_evaluation == None:
        return False
        
    date = user_evaluation.assigned_date

    
    rules = CalendarOrderable.objects.all()
    for rule in rules:

        if rule.calendar == 'day':
            ending_date = date + timedelta(days=rule.count)
        if rule.calendar == 'week':
            ending_date = date + timedelta(days=rule.count * 7)
        if rule.calendar == 'month':
            ending_date = date + timedelta(days=rule.count * 30)
        if rule.calendar == 'year':
            ending_date = date + timedelta(days=rule.count * 365)

        if ending_date > timezone.now():
            return True

    return False

@register.simple_tag
def check_status(user_evaluation):
    
    if user_evaluation == None:
        return None

    if user_evaluation.submit_date :
        return 'done-evaluating'
    else:
        return 'for-evaluation'

@register.simple_tag
def client_status(client):
    user_evaluations = client.user_evaluation.all()
    
    if user_evaluations == None:
        return None
    
    for_evaluation = user_evaluations.filter(submit_date__isnull=True)

    if for_evaluation:
        return {
            'status': 'for-evaluation',
            'count': len(for_evaluation)
        }
    else:
        return { 
            'status' : 'done-evaluating'
        }
    
    
