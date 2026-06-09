from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
from database.db import DatabaseManager

# Create your views here.


def login_view(request):
    # Paso 1: verificar existencia de una session activa
    if 'user_rut' in request.session:
        # Redireccionar según ROL:
        rol_actual = request.session.get('user_rol')
        if rol_actual == 'Admin':
            return redirect('core:admin_dash')
        if rol_actual == 'Recepcionista':
            return redirect('core:recepcion_dash')
        if rol_actual == 'Cliente':
            return redirect('core:cliente_dash')

    if request.method == 'POST':
        # Paso 2: capturar datos del formulario login, y definir variables
        usuario_login = request.POST.get('usuario')  # Email o RUT
        password_login = request.POST.get('password')
        user_found = None
        context = {}
        db = DatabaseManager()

        # Buscar el usuario en la DB
        try:
            # Necesitamos un LEFT JOIN para 'membresías' porque tenemos algunos
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
                WHERE (u.email = %s OR u.rut = %s) AND u.is_active = 1;
            """

            user_found = db.get_one(
                query_search_user, (usuario_login, usuario_login))
        except Exception as e:
            print(f"ERROR CRITICO DB [Buscar Usuario]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error del Sistema',
                    'message': 'No pudimos conectar con la base de datos. Intente mas tarde.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # Paso 3: funcion para registrar una auditoria
        def insert_auditoria(usuario_ingresado, estado_login, password_ingresada=None):
            try:
                query_auditoria = """
                    INSERT INTO auditoria_login
                    (usuario, estado_login, password_ingresada)
                    VALUES (%s, %s, %s);
                """

                db.execute(query_auditoria, (usuario_ingresado,
                           estado_login, password_ingresada))
            except Exception as e:
                print(
                    f"ADVERTENCIA DB [Auditoria]: No se pudo guardar el registro: {str(e)}")
                pass

        # Paso 4: manejar los diferentes casos respecto al resultado de la busqueda del usuario en DB
        # CASO 1: usuario NO registrado en la DB
        if not user_found:
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'No existe un registro asociado a ese rut/email/contraseña.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 1.2: usuario es INVITADO, no puede realizar login
        if user_found and user_found['rol_nombre'] == 'Invitado':
            context = {
                'sw_alert': {
                    'type': 'warning',
                    'title': 'Acceso Denegado',
                    'message': 'Las cuentas de tipo Invitado no tienen permisos para acceder al sistema. Hable con un Administrador.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 2: existe un usuario registrado asociado al rut/email, pero no esta disponible...
        # CASO 2.1: usuario registrado pero bloqueado por seguridad
        if user_found['intentos_fallidos'] == 3 or user_found['estado_usuario_id'] == 4:
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'Usuario Bloqueado por Seguridad, comunicarse con un Administrador.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 2.2: usuario registrado pero bloqueado por deuda
        if user_found['estado_usuario_id'] == 3:
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'Usuario Bloqueado por Deuda, por favor pague su deuda.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 2.3: usuario registrado pero inactivo
        if user_found['estado_usuario_id'] == 2:
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'Usuario Inactivo, comunicarse con un Administrador.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 3: existe usuario, comparamos los datos...
        password_hash_db = user_found['password']

        # CASO 3.1: las passwords NO coinciden
        if not check_password(password_login, password_hash_db):
            # Auditoria
            insert_auditoria(usuario_login, 'Incorrecto', password_login)

            # calcular valor real de intentos
            nuevos_intentos = user_found['intentos_fallidos'] + 1

            try:
                # Actualizar contador de intentos fallidos en la DB
                query_update_intentos_fallidos = """
                    UPDATE usuarios
                    SET intentos_fallidos = %s
                    WHERE rut = %s;
                """
                db.execute(query_update_intentos_fallidos,
                           (nuevos_intentos, user_found['rut']))

                # Bloqueo por seguridad al tener mas de 3 intentos fallidos
                if nuevos_intentos >= 3:
                    query_update_estado_usuario = """
                        UPDATE usuarios
                        SET estado_usuario_id = 4
                        WHERE rut = %s;
                    """

                    db.execute(query_update_estado_usuario,
                               (user_found['rut'],))
            except Exception as e:
                print(
                    f"ADVERTENCIA DB [Actualizar Intentos]: No se pueden actualizar los intentos: {str(e)}")
                pass

            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'Usuario y/o contraseña inválidos.'
                }
            }
            return render(request, 'authentication/login.html', context)

        # CASO 3.2: las passwords SI coinciden
        if check_password(password_login, password_hash_db):
            # Auditoria
            insert_auditoria(usuario_login, 'Correcto')

            # Actualizar intentos_fallidos a 0
            try:
                query_update_intentos_fallidos = """
                    UPDATE usuarios
                    SET intentos_fallidos = 0
                    WHERE rut = %s;
                """

                db.execute(query_update_intentos_fallidos,
                           (user_found['rut'],))
            except Exception as e:
                print(
                    f"ADVERTENCIA DB [Actualizar Intentos]: No se pueden actualizar los intentos: {str(e)}")
                pass

            # Crear SESION
            request.session['user_rut'] = user_found['rut']
            request.session['user_email'] = user_found['email']
            request.session['user_nombres'] = user_found['nombres']
            request.session['user_apellidos'] = user_found['apellidos']
            request.session['user_rol'] = user_found['rol_nombre']
            request.session['user_membresia'] = user_found['membresia_nombre']

            # Dependiendo del ROL redireccionar al dashboard/vista respectiva
            rol_asignado = user_found['rol_nombre']
            if rol_asignado == 'Admin':
                return redirect('core:admin_dash')
            if rol_asignado == 'Recepcionista':
                return redirect('core:recepcion_dash')
            if rol_asignado == 'Cliente':
                return redirect('core:cliente_dash')

    return render(request, 'authentication/login.html')


def logout_view(request):
    request.session.flush()  # borrar sesion
    return redirect('authentication:login')


def register_view(request):
    # Paso 1: verificar existencia de una session activa
    if 'user_rut' in request.session:
        # Redireccionar segun ROL:
        rol_actual = request.session.get('user_rol')
        if rol_actual == 'Admin':
            return redirect('core:admin_dash')
        if rol_actual == 'Recepcionista':
            return redirect('core:recepcion_dash')
        if rol_actual == 'Cliente':
            return redirect('core:cliente_dash')

    message = None
    context = {}

    if request.method == 'POST':
        # Capturar datos del registro
        rut = request.POST.get('rut')
        nombres = request.POST.get('nombres')
        apellido_p = request.POST.get('apellido_p')
        apellido_m = request.POST.get('apellido_m')
        email = request.POST.get('email')
        password = request.POST.get('password')

        db = DatabaseManager()

        try:
            # Validar duplicados
            valid_rut = db.exists(
                'SELECT rut FROM usuarios WHERE rut = %s;', (rut,))
            valid_email = db.exists(
                'SELECT email FROM usuarios WHERE email = %s;', (email,))

            if valid_rut:
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'RUT Duplicado',
                        'message': 'El RUT ya se encuentra registrado.'
                    }
                }
            elif valid_email:
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Email en uso',
                        'message': 'El Email ya esta registrado.'
                    }
                }
            else:
                # Registrar usuario
                password_hashed = make_password(password)

                query_add_user = """
                    INSERT INTO usuarios
                    (rut, nombres, apellido_p, apellido_m, email, password, estado_usuario_id, rol_id, membresia_id)
                    VALUES (%s, %s, %s, %s, %s, %s, 1, 3, 1)
                """

                db.execute(query_add_user, (rut, nombres, apellido_p,
                           apellido_m, email, password_hashed))

                context = {
                    'sw_alert': {
                        'type': 'success',
                        'title': 'Registro Exitoso!',
                        'message': 'Ya puedes iniciar sesión con tus credenciales.',
                        'redirect': reverse('authentication:login')
                    }
                }
        except Exception as e:
            print(f"ERROR CRITICO [Registrar Usuario]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error del Sistema',
                    'message': 'No pudimos procesar tu registro. Intente mas tarde.'
                }
            }

    return render(request, 'authentication/register.html', context)
