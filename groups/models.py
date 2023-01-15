from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    group_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
    users = models.ManyToManyField(to=User, blank=True)
    is_room = models.BooleanField()
    # api = models.ForeignKey(to="main.API", on_delete=models.RESTRICT)
