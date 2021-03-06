from django import template

from performance_management_system.base.models import Notification

register = template.Library()

@register.simple_tag
def notication_count(reciever):
    return len(Notification.objects.filter(reciever_id=reciever, seen=False))

@register.simple_tag
def for_evaluation_count(reciever):

    evaluation = reciever.user_evaluation.filter(submit_date__isnull=True)

    return len(evaluation)

@register.simple_tag
def get_latest_notif_date(user, notification_type):
    get_notifications = user.notifications.filter(notification_type=notification_type)

    if len(get_notifications) <= 0:
        return None

    get_latest_notif = get_notifications.latest('created_at')
    
    if get_latest_notif == None:
        return None

    return get_latest_notif.created_at
