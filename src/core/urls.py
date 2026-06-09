from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', views.admin_view, name='admin_dash'),
    path('reception/', views.recepcion_view,
         name='recepcion_dash'),
    path('client/', views.cliente_view, name='cliente_dash'),
]
