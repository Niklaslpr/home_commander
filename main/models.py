from django.db import models
from django.utils.translation import gettext_lazy as _


class LogEntry(models.Model):
    class LogType(models.TextChoices):
        DEVICE_STATE_CHANGE = 'dsc', _('state of device changed')
        OTHER = 'etc', _('non specified')

    type = models.CharField(max_length=3, choices=LogType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=256)
