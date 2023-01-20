from django.contrib.auth.models import User
from django.db import models


class Scene(models.Model):
    group_id = models.CharField(max_length=64)
    scene_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
    users = models.ManyToManyField(to=User, blank=True)
    
