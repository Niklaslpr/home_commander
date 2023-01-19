# Generated by Django 4.1 on 2023-01-15 14:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("device_id", models.CharField(max_length=64)),
                ("name", models.CharField(max_length=64)),
                ("icon", models.CharField(max_length=255)),
                (
                    "device_type",
                    models.CharField(
                        choices=[("l", "light"), ("s", "sensor")], max_length=1
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
