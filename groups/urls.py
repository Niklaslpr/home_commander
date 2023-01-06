from django.urls import path

from . import views

urlpatterns = [
    path('', views.groups, name='groups'),
    path('grouponoff/', views.grouponoff, name='grouponoff'),
    path('creategroup/', views.creategroup, name='creategroup'),
    path('group_info/all', views.get_all_group_data, name='get_all_group_data'),
    path('group_info/<str:id>', views.get_group_data, name='get_group_data'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
]
