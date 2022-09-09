from django.db import models
import pytz
from django.utils import timezone
from .utils import get_phone_regex_validator


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.CharField(validators=[get_phone_regex_validator()], max_length=11, unique=True)
    operator_code = models.CharField(editable=False, max_length=3)
    tag = models.CharField(blank=True, max_length=128)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)


class Mailing(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    text = models.TextField()
    filter_tag = models.CharField(max_length=128, blank=True)
    filter_code = models.CharField(max_length=3, blank=True)

    @property
    def is_due(self):
        now = timezone.now()
        if self.start_datetime <= now <= self.end_datetime:
            return True
        else:
            return False


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
