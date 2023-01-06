from django.urls import path
from . import views

urlpatterns = [
    path('', views.scenes, name='scenes'),
    path('scene_info/all', views.get_all_scene_data, name='get_all_scene_data'),
    path('scene_info/<str:id>', views.get_scene_data, name='get_scene_data'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
]