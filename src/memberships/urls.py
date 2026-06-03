from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('', views.membership_list, name='membership_list'),
    path('create/', views.membership_create, name='membership_create'),
    path('edit/<int:membresia_id>/', views.membership_update, name='membership_update'),
    path('delete/<int:membresia_id>/', views.membership_delete, name='membership_delete'),
]
