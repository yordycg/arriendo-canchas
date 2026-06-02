from django.urls import path
from . import views

app_name = 'courts'

urlpatterns = [
    path('', views.court_list, name='court_list'),
    path('create/', views.court_create, name='court_create'),
    path('pavilions/create/', views.pavilion_create, name='pavilion_create'),
]
