from django.urls import path

from . import views
from devices import views as views2

urlpatterns = [
    path('', views.groups, name='groups'),
    path('grouponoff/', views.grouponoff, name='grouponoff'),
    path('creategroup/', views.creategroup, name='creategroup'),
    path('updategroup/', views.updategroup, name='updategroup'),
    path('deletegroup/', views.deletegroup, name='deletegroup'),
    path('groupsethue/', views.groupsethue, name='groupsethue'),
    path('groupsetbri/', views.groupsetbri, name='groupsetbri'),
    path('group_info/all', views.get_all_group_data, name='get_all_group_data'),
    path('group_info/<str:id>', views.get_group_data, name='get_group_data'),
    path('group_change/', views.modify_group, name='modify_group'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
    
]
