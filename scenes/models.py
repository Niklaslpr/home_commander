from django.contrib.auth.models import User
from django.db import models


class Scene(models.Model):
    scene_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
    users = models.ManyToManyField(to=User, blank=True)
    api = models.ForeignKey(to="main.API", on_delete=models.RESTRICT,
                            default="main.API.objects.get(name__exact=='DECONZ')")
