# tester/urls.py
from django.urls import path
from . import views

# tester/urls.py
urlpatterns = [
    path('', views.server_list, name='server_list'),
    path('add/', views.add_server, name='add_server'),
    path('test/<int:server_id>/', views.test_server, name='test_server'),
    path('modify/<int:server_id>/', views.modify_server, name='modify_server'),
    path('delete/<int:server_id>/', views.delete_server, name='delete_server'),
]
