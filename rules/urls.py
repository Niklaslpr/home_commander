from django.urls import path

from . import views

urlpatterns = [
    path('', views.rules, name='rules'),
    path('createschedule/', views.createschedule, name='createschedule'),
    path('create_rule', views.create_rule, name='create_rule'),
    path('update_rule', views.update_rule, name='update_rule'),
    path('delete_rule', views.delete_rule, name='delete_rule'),
    path('rule_info/all', views.get_all_rule_data, name='get_all_rule_data'),
    path('rule_info/<str:id>', views.get_rule_data, name='get_rule_data'),
    path('kit/<str:kit_name>', views.kits, name='kits'),
]
