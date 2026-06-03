from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('', views.membership_list, name='membership_list'),
]
