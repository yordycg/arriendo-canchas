from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('', views.membership_list, name='membership_list'),
    path('create/', views.membership_create, name='membership_create'),
]
