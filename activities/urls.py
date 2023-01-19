from django.urls import path
from . import views

urlpatterns = [
    path('', views.activities, name='activities'),
    path('load_logs', views.load_logs, name='load_logs'),
]
