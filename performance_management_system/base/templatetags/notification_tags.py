from django import template

from performance_management_system.base.models import Notification

register = template.Library()

@register.simple_tag
def notication_count(reciever):
    return len(Notification.objects.filter(reciever_id=reciever, seen=False))