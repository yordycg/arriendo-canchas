from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('form/', views.user_form, name='user_form'),
    path('create/', views.user_create, name='user_create'),
    path('delete/', views.user_delete, name='user_delete')
]
