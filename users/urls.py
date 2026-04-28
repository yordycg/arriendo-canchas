from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('form/', views.user_form),
    path('add/', views.add_user)
]
