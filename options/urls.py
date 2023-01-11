from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings, name='options'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('delete_user/', views.delete_user, name='delete_user'),
]