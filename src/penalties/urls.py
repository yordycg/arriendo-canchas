from django.urls import path
from . import views

app_name = 'penalties'

urlpatterns = [
    path('', views.penalty_list, name='penalty_list'),
    path('pay/<int:penalty_id>/', views.penalty_pay, name='penalty_pay'),
    path('delete/<int:penalty_id>/', views.penalty_delete, name='penalty_delete'),
    path('my-penalties/', views.my_penalties, name='my_penalties'),
]
