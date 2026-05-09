from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def login_required_manual(view_func):
    """
    Decorador para verificar si el usuario tiene una sesión activa.
    Busca la existencia de 'user_rut' en la sesión.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_rut' not in request.session:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('authentication:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(allowed_roles: list):
    """
    Decorador para restringir el acceso basado en el rol del usuario.
    Ejemplo de uso: @role_required(['Administrador', 'Vendedor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Verificar primero si está logueado
            if 'user_rut' not in request.session:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('authentication:login')

            # 2. Verificar si su rol está en la lista de permitidos
            user_rol = request.session.get('user_rol')
            if user_rol not in allowed_roles:
                messages.warning(request, f'Acceso denegado. Se requiere el rol: {", ".join(allowed_roles)}')
                return redirect('users:user_list')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
