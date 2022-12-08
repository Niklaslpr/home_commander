from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('weather/', views.weather, name='weather'),
    path('devices/', views.devices, name='devices'),
    path('turnonoff/', views.turnonoff, name='turnonoff'),
    path('setbri/', views.setbri, name='setbri'),
    path('sethue/', views.sethue, name='sethue'),
    path('device_info/all', views.get_all_device_data, name='get_all_device_data'),
    path('device_info/<str:id>', views.get_device_data, name='get_device_data'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
    path('startsearch/', views.startsearch, name='startsearch'),
    path('activities/', views.activities, name='activities'),
    path('rooms/', views.rooms, name='rooms'),
    path('scenes/', views.scenes, name='scenes'),
    path('options/', views.options, name='options'),
    path('rules/', views.rules, name='rules'),
    path('createschedule/', views.createschedule, name='createschedule'),
    path('groups/', views.groups, name='groups'),
    path('grouponoff/', views.grouponoff, name='grouponoff'),
    path('creategroup/', views.creategroup, name='creategroup'),
]