from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

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
 
@register.filter(name='user_evaluation_data_filter') 
def user_evaluation_data_filter(user_evaluation):   
    return serializers.serialize("json", user_evaluation,cls=DjangoJSONEncoder)