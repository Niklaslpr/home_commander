from django.urls import path
from . import views
from devices import views as views2


urlpatterns = [
    path('', views.home, name='home'),
    path('weather/', views.weather, name='weather'),
    path('createFavoriteGroup/', views.createFavoriteGroup, name='createFavoriteGroup'),
    path('isDeviceinFavorites/', views.isDeviceinFavorites, name='isDeviceinFavorites'),
    path('kit/<str:kit_name>', views2.kits, name='kits'),
    path('deleteDeviceFromFavorites/', views2.deleteDeviceFromFavorites, name='deleteDeviceFromFavorites'),
    path('turnonoff/', views2.turnonoff, name='turnonoff'),
    path('setbri/', views2.setbri, name='setbri'),
    path('sethue/', views2.sethue, name='sethue'),
]
