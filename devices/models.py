from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Device(models.Model):
    class DeviceType(models.TextChoices):
        LIGHT = 'l', _('light')
        SENSOR = 's', _('sensor')

    device_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
    device_type = models.CharField(max_length=1, choices=DeviceType.choices)
    # type = models.CharField(max_length=32)
    users = models.ManyToManyField(to=User)
