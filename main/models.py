from django.contrib.auth.models import User
from django.db import models
from devices.models import Device
from groups.models import Group
from rooms.models import Room
from scenes.models import Scene


class Favourite(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(to=Device)
    groups = models.ManyToManyField(to=Group)
    rooms = models.ManyToManyField(to=Room)
    scenes = models.ManyToManyField(to=Scene)
