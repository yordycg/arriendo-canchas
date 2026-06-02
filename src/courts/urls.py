from django.urls import path
from . import views

app_name = 'courts'

urlpatterns = [
    path('', views.court_list, name='court_list'),
    # Próximamente: create, update, delete
]
