from django.urls import path
from . import views

urlpatterns = [
    path('', views.devices, name='devices'),
    path('turnonoff/', views.turnonoff, name='turnonoff'),
    path('setbri/', views.setbri, name='setbri'),
    path('sethue/', views.sethue, name='sethue'),
    path('device_info/all', views.get_all_device_data, name='get_all_device_data'),
    path('device_info/<str:id>', views.get_device_data, name='get_device_data'),
    path('device_change/', views.modify_device, name='modify_device'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
    path('startsearch/', views.startsearch, name='startsearch'),
    path('addDeviceToFavorites/', views.addDeviceToFavorites, name='addDeviceToFavorites'),
    path('deleteDeviceFromFavorites/', views.deleteDeviceFromFavorites, name='deleteDeviceFromFavorites'),
    path('isDeviceinFavorites/', views.isDeviceinFavorites, name='isDeviceinFavorites'),
    path('deleteDevice/', views.deleteDevice, name='deleteDevice'),
]
