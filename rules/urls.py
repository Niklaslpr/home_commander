from django.urls import path
from . import views

urlpatterns = [
    path('rules/', views.rules, name='rules')
]