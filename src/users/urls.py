from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('update/<str:rut>/', views.user_update, name='user_update'),
    path('delete/<str:rut>/', views.user_delete, name='user_delete'),
    path('profile/', views.profile, name='profile'),
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dash'),
    # path('recepcion-dashboard/', views.recepcionista_dashboard,
    #      name='recepcionista_dash'),
    # path('cliente-dashboard/', views.cliente_dashboard, name='cliente_dash'),
]
