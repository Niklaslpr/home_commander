from django.db import models
from django.contrib.auth.models import User


class Scene(models.Model):
    scene_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
    users = models.ManyToManyField(to=User)
