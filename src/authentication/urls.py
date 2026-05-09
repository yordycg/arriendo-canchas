from django.urls import path
from . import views

# Namespacing, forma de ser mas especifico dando un 'apellido' a las rutas.
# Evitamos las colisiones de nombre (Por ejemplo: users.home != auth.home)
app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]