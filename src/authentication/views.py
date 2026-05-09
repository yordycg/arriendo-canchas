from django.shortcuts import redirect, render
from django.http import HttpResponse
from database.db import DatabaseManager

# Create your views here.
def login_view(request):
    """
    1.- Obtener los datos de login (correo/rut y password) por medio de POST.get.
    2.- Conectarme a la DB y por el rut, que is_active esta en 1, buscar el usuario.
        SI NO existe:
            retorno alerta(usuario no registrado) | redireccionar al formulario de registrar usuario (?)
        SI existe:
            Pero intentos_fallidos = 3 Y/O estado_usuario = bloqueado por seguridad Y/O estado_usuario = inactivo:
                retorno alerta(usuario bloqueado por seguridad) | redireccionar -> comunicarse con admin (?)
            Pero estado_usuario = bloqueado por deuda:
                retorno alerta(usuario tiene una deuda) | redirecciono -> metodos de pagos (?)
    3.- Comparar los datos de la DB vs obtenidos por el form-login:
        SI email/rut = db.email/rut Y pass = db.pass Y estado_usuario = activo:
            intentos_fallidos = 0
            Crear SESION:
                - rut
                - nombre completo
                - rol_id
            retorno | redireccionar a donde tu tipo_rol lo permita..
        SI email/rut = db.email/rut Y pass != db.pass:
            intentos_fallido ++
            SI intentos_fallidos = 3:
                estado_usuario.bloqueo_seguridad = true
    """
    if request.method == 'POST':
        # Obtener los datos del form-login
        email = request.POST.get('email')
        password_hashed = request.POST.get('password')

        # Conectarme a la DB y buscar el usuario...
        db = DatabaseManager()

        # TODO: debemos buscar por rut o email?
        # Necesitamos un LEFT JOIN para 'membresias' porque tenemos algunos
        # roles que permiten valores NULL, pero de igual forma debemos obtenerlos
        query_search_user = """
            SELECT
                rut,
                nombres,
                CONCAT(apellido_p, ' ', apellido_m) AS apellidos,
                email,
                password,
                intentos_fallidos,
                estado_usuario_id,
                r.nombre AS rol_nombre,
                m.nombre AS membresia_nombre
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.rol_id
            LEFT JOIN membresias m ON u.membresia_id = m.membresia_id
            WHERE u.email = %s AND u.is_active = 1;
        """

        user_found = db.get_one(query_search_user, (email,))

        # CASO 1: usuario NO registrado en la DB
        if not user_found:
            context = {
                'error': 'No existe un registro asociado a ese email.'
            }
            return render(request, 'authentication/login.html', context)

        # CASO 2: existe un usuario registrado asociado a ese 'email'
        if user_found:
            # CASO 2.1: usuario registrado pero, intentos_fallidos = 3
            # O estado = bloqueado_seguridad O estado = inactivo
            if user_found['intentos_fallidos'] == 3 or user_found['estado_usuario_id'] == 4 or user_found['estado_usuario_id'] == 2:
                context = {
                    'error': 'Usuario Bloqueado Por Seguridad o Inactivo, comunicarse con un ADMIN.'
                }
                return render(request, 'authentication/login.html', context)

            # CASO 2.2: usuario registrado pero bloqueado por deuda
            if user_found['estado_usuario_id'] == 3:
                context = {
                    'error': 'Usuario bloqueado por deuda.'
                }
                return render(request, 'authentication/login.html', context)

            # CASO 3: comparar los datos de la DB con los del LOGIN
            # CASO 3.1: usuario.pass es diferente al login.pass
            # TODO: hashear (?) la password...
            if user_found['password'] != password_hashed:
                # Calcular valor REAL de itentos_fallidos
                nuevos_intentos = user_found['intentos_fallidos'] + 1

                # Actualizar contador de intentos fallidos en la DB
                query_update_intentos_fallidos = """
                    UPDATE usuarios
                    SET intentos_fallidos = %s
                    WHERE rut = %s;
                """
                db.execute(query_update_intentos_fallidos, (nuevos_intentos, user_found['rut']))

                # Bloquear usuario por seguridad al tener mas de 3
                # intentos fallidos
                if nuevos_intentos >= 3:
                    query_update_estado_usuario = """
                        UPDATE usuarios
                        SET estado_usuario_id = 4
                        WHERE rut = %s;
                    """

                    db.execute(query_update_estado_usuario, (user_found['rut'],))

                context = {
                    'error': 'Usuario y/o contrasena invalidos.'
                }
                return render(request, 'authentication/login.html', context)

            # CASO 3.2: usuario.pass_hashed es igual al login.pass_hashed
            if user_found['password'] == password_hashed:
                # Actualizar intentos_fallidos a 0
                intentos_fallidos = 0

                query_update_intentos_fallidos = """
                    UPDATE usuarios
                    SET intentos_fallidos = 0
                    WHERE rut = %s;
                """

                db.execute(query_update_intentos_fallidos, (user_found['rut'],))

                # Crear SESION
                # TODO: como gestionar el rol y membresia, deberiamos haber hecho un JOIN antes??
                request.session['user_rut'] = user_found['rut']
                request.session['user_nombres'] = user_found['nombres']
                request.session['user_apellidos'] = user_found['apellidos']
                request.session['user_rol'] = user_found['rol_nombre']
                request.session['user_membresia'] = user_found['membresia_nombre']

                # Redireccionar al home del usuario
                return redirect('users:user_list')

            # TODO: enviar el 'context' para mostrar en las alertas
            return render(request, 'authentication/login.html', context)

    return render(request, 'authentication/login.html')

def logout_view(request):
    request.session.flush() # borrar sesion
    return redirect('authentication:login')



