from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import pytz

class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)


    @property
    def profile_pic(self):
        try:
            if self.is_client:
                return self.client.profile_pic.get_rendition('fill-50x50').img_tag()
            if self.is_employee:
                return self.employee.profile_pic.get_rendition('fill-50x50').img_tag()
            if self.is_hr:
                return self.hradmmin.profile_pic.get_rendition('fill-50x50').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''
    
        

    @property
    def latest_login(self):
        if self.last_login:
            return timezone.localtime(self.last_login, pytz.timezone('Asia/Singapore')).strftime('%I:%M %p %b %d, %Y')
        return None

    @property
    def name(self):
        if self.is_client:
            return self.client.company

        if self.is_employee:
            return self.employee.last_name + ', ' + self.employee.first_name + ' ' + self.employee.middle_name

        return ''