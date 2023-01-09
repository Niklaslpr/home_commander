from django.urls import path
from . import views

urlpatterns = [
    path('options/', views.settings, name='options'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
]