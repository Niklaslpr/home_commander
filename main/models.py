from django.contrib.auth.models import User
from django.db import models
from devices.models import Device
from groups.models import Group
from rooms.models import Room
from scenes.models import Scene


class Favourite(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(to=Device, blank=True)
    groups = models.ManyToManyField(to=Group, blank=True)
    rooms = models.ManyToManyField(to=Room, blank=True)
    scenes = models.ManyToManyField(to=Scene, blank=True)


class API(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
