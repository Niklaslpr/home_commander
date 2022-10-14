from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('turnonoff/', views.turnonoff, name='turnonoff'),
    path('setbri/', views.setbri, name='setbri'),
    path('sethue/', views.sethue, name='sethue'),
]