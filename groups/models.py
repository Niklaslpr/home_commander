from django.db import models


class Group(models.Model):
    group_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=255)
