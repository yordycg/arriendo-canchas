from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from database.db import DatabaseManager

# Create your views here.
def login_view(request):
    if 'user_rut' in request.session:
        return redirect('users:user_list')

    if request.method == 'POST':
        # Obtener los datos del form-login
        email_login = request.POST.get('email')
        password_login = request.POST.get('password')

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

        user_found = db.get_one(query_search_user, (email_login,))

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

            password_hash_db = user_found['password']

            if not check_password(password_login, password_hash_db):
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
            if check_password(password_login, password_hash_db):
                # Actualizar intentos_fallidos a 0
                query_update_intentos_fallidos = """
                    UPDATE usuarios
                    SET intentos_fallidos = 0
                    WHERE rut = %s;
                """

                db.execute(query_update_intentos_fallidos, (user_found['rut'],))

                # Crear SESION
                request.session['user_rut'] = user_found['rut']
                request.session['user_nombres'] = user_found['nombres']
                request.session['user_apellidos'] = user_found['apellidos']
                request.session['user_rol'] = user_found['rol_nombre']
                request.session['user_membresia'] = user_found['membresia_nombre']

                # Redireccionar al home del usuario
                return redirect('users:user_list')

            return render(request, 'authentication/login.html', context)

    return render(request, 'authentication/login.html')

def logout_view(request):
    request.session.flush() # borrar sesion
    return redirect('authentication:login')

def register_view(request):
    # Si una sesion esta activa (logueado), redireccionamos al inicio
    if 'user_rut' in request.session:
        return redirect('users:user_list')

    error = None

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombres = request.POST.get('nombres')
        apellido_p = request.POST.get('apellido_p')
        apellido_m = request.POST.get('apellido_m')
        email = request.POST.get('email')
        password = request.POST.get('password')

        db = DatabaseManager()

        # Validar RUT y EMAIL
        valid_rut = db.exists('SELECT rut FROM usuarios WHERE rut = %s;', (rut,))
        valid_email = db.exists('SELECT email FROM usuarios WHERE email = %s;', (email,))

        if valid_rut:
            error = 'El RUT ya esta registrado.'
        elif valid_email:
            error = 'El CORREO ya esta en uso.'
        else:
            try:
                password_hashed = make_password(password)

                query_add_user = """
                    INSERT INTO usuarios
                    (rut, nombres, apellido_p, apellido_m, email, password, estado_usuario_id, rol_id, membresia_id)
                    VALUES (%s, %s, %s, %s, %s, %s, 1, 3, 1)
                """

                db.execute(query_add_user, (rut, nombres, apellido_p, apellido_m, email, password_hashed))

                return redirect('authentication:login')

            except Exception as e:
                error = f'Error al registrar: {str(e)}'

    context = {
        'error': error
    }

    return render(request, 'authentication/register.html', context)


