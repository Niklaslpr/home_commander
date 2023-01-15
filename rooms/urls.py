from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('room_info/all', views.get_all_room_data, name='get_all_room_data'),
    path('room_info/<str:id>', views.get_room_data, name='get_room_data'),
    path('room_change/', views.modify_room, name='modify_room'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
]
