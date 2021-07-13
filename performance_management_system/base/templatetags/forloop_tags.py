from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from performance_management_system import GRADIENT_BG

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


@register.filter(name='gradient_bg')
def  gradient_bg(id):
    return 'background-image: linear-gradient('+GRADIENT_BG[id-1][0]+','+ GRADIENT_BG[id-1][1]+')'

