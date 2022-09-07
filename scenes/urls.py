from django.urls import path
from . import views

urlpatterns = [
    path('scenes/', views.scenes, name='scenes')
]