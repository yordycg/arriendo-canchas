from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required

# Create your views here.


@login_required_manual
def user_list(request):
    db = DatabaseManager()
    context = {}

    try:
        query_all_usuarios = """
            SELECT
                u.rut,
                u.nombres,
                u.apellido_p,
                u.apellido_m,
                u.sexo,
                u.telefono,
                u.email,
                eu.nombre as estado_usuario,
                r.nombre as rol,
                COALESCE(m.nombre, 'Sin Membresia') AS membresia -- COALESCE por si es NULL
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.rol_id
            JOIN estados_usuarios eu ON u.estado_usuario_id = eu.estado_usuario_id
            LEFT JOIN membresias m ON u.membresia_id = m.membresia_id
            WHERE u.is_active = 1; -- Solo usuarios activos
        """

        users = db.get_all(query_all_usuarios)

        context = {
            'usuarios': users
        }
        return render(request, 'users/home.html', context)
    except Exception as e:
        print(f"ERROR CRITICO DB [Usuarios]: {str(e)}")
        context = {
            'sw_alert': {
                'type': 'error',
                'title': 'Error del Sistema',
                'message': 'No pudimos conectar con la base de datos. Intente mas tarde.',
            }
        }
        return render(request, 'users/home.html', context)


@login_required_manual
@role_required(['Admin'])
def user_create(request):
    db = DatabaseManager()
    context = {}
    roles = db.get_all('SELECT rol_id, nombre FROM roles;')
    estados_usuarios = db.get_all(
        'SELECT estado_usuario_id, nombre FROM estados_usuarios;')
    membresias = db.get_all('SELECT membresia_id, nombre FROM membresias;')

    def get_dropdown_data():
        return {
            'roles': roles,
            'estados': estados_usuarios,
            'membresias': membresias
        }

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombres = request.POST.get('nombres')
        apellido_p = request.POST.get('apellido_p')
        apellido_m = request.POST.get('apellido_m')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hashed = make_password(password)  # generar hash
        sexo = request.POST.get('sexo')
        telefono = request.POST.get('telefono')
        estado_usuario_id = int(request.POST.get('estado_usuario_id'))
        rol_id = int(request.POST.get('rol_id'))
        membresia_raw = request.POST.get('membresia_id')

        # Validar el rol_id, para evitar asignar una membresia_id al 'admin' e 'invitado'
        if rol_id in [1, 4]:
            membresia_id = None
        else:
            # Si viene vacio, de forma default asignamos membresia 'Normal'
            membresia_id = int(membresia_raw) if membresia_raw else 1

        try:
            # Validar que no exista el 'rut' a ingresar
            query_validar_rut = 'SELECT * FROM usuarios WHERE rut = %s;'

            if db.exists(query_validar_rut, (rut,)):
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Rut Existente',
                        'message': 'Ya existe un registro asociado a ese RUT.'
                    },
                    # Recargar los selects:
                    # Usamos el operador '**' para desempaquetar los diccionarios en python,
                    # Asi podemos vaciar el contenido de un diccionario dentro de otro diccionario.
                    **get_dropdown_data()
                }
                return render(request, 'users/user_form.html', context)
            else:
                query_add_user = """
                    INSERT INTO usuarios
                    (rut, nombres, apellido_p, apellido_m, email, password, sexo, telefono, estado_usuario_id, rol_id, membresia_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
                params = (rut, nombres, apellido_p, apellido_m, email, password_hashed,
                          sexo, telefono, estado_usuario_id, rol_id, membresia_id)

                db.execute(query_add_user, params)

                context = {
                    'sw_alert': {
                        'type': 'success',
                        'title': 'Registro Exitoso!',
                        'message': 'Felicidades, usuario registrado correctamente.',
                        'redirect': reverse('users:user_list')
                    }
                }
                return render(request, 'users/user_form.html', context)
        except Exception as e:
            print(
                f"ERROR DB [Crear Usuario]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Registro',
                    'message': 'No se pudo crear el usuario. Revise los datos.'
                },
                **get_dropdown_data()
            }
            return render(request, 'users/user_form.html', context)

    # Metodo GET
    return render(request, 'users/user_form.html', get_dropdown_data())


@login_required_manual
@role_required(['Admin'])
def user_delete(request, rut):
    try:
        pass
        db = DatabaseManager()

        # SOFT-DELETE: marcar como inactivo
        query_delete = "UPDATE usuarios SET is_active = 0 WHERE rut = %s;"

        db.execute(query_delete, (rut,))

        return redirect('users:user_list')
    except Exception as e:
        print(f"ADVERTENCIA DB [Eliminar Usuario]: {str(e)}")
        pass


@login_required_manual
@role_required(['Admin'])
def user_update(request, rut):
    db = DatabaseManager()
    context = {}
    roles = db.get_all('SELECT rol_id, nombre FROM roles;')
    estado_usuarios = db.get_all(
        'SELECT estado_usuario_id, nombre FROM estados_usuarios;')
    membresias = db.get_all('SELECT membresia_id, nombre FROM membresias;')

    def get_dropdown_data():
        return {
            'roles': roles,
            'estados': estado_usuarios,
            'membresias': membresias
        }

    # Gestionar el guardado en la db
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellido_p = request.POST.get('apellido_p')
        apellido_m = request.POST.get('apellido_m')
        email = request.POST.get('email')
        # Capturamos la posible nueva password
        password = request.POST.get('password')
        sexo = request.POST.get('sexo')
        telefono = request.POST.get('telefono')
        estado_usuario_id = int(request.POST.get('estado_usuario_id'))
        rol_id = int(request.POST.get('rol_id'))
        membresia_raw = request.POST.get('membresia_id')

        # Validar el rol_id, para evitar asignar una membresia_id al 'admin' e 'invitado'
        if rol_id in [1, 4]:
            membresia_id = None
        else:
            # Si viene vacio, de forma default asignamos membresia 'Normal'
            membresia_id = int(membresia_raw) if membresia_raw else 1

        try:
            # Lógica para actualización opcional de password
            if password and password.strip():
                # Si el admin escribió una nueva password, la hasheamos e incluimos
                password_hashed = make_password(password)
                query_update = """
                    UPDATE usuarios
                    SET nombres=%s, apellido_p=%s, apellido_m=%s,
                    email=%s, sexo=%s, telefono=%s,
                    estado_usuario_id=%s, rol_id=%s, membresia_id=%s,
                    password=%s
                    WHERE rut=%s;
                """
                params = (nombres, apellido_p, apellido_m, email, sexo, telefono,
                          estado_usuario_id, rol_id, membresia_id, password_hashed, rut)
            else:
                # Si el campo está vacío, NO tocamos la password actual
                query_update = """
                    UPDATE usuarios
                    SET nombres=%s, apellido_p=%s, apellido_m=%s,
                    email=%s, sexo=%s, telefono=%s,
                    estado_usuario_id=%s, rol_id=%s, membresia_id=%s
                    WHERE rut=%s;
                """
                params = (nombres, apellido_p, apellido_m, email, sexo, telefono,
                          estado_usuario_id, rol_id, membresia_id, rut)

            db.execute(query_update, params)

            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': 'Actualización Exitosa!',
                    'message': 'Los datos del usuario han sido actualizados correctamente.',
                    'redirect': reverse('users:user_list')
                }
            }
            return render(request, 'users/user_form.html', context)
        except Exception as e:
            print(f"Error al actualizar [Usuario]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Actualización',
                    'message': 'No se pudieron guardar los cambios. Intente más tarde.'
                },
                'usuario': {
                    'rut': rut, 'nombres': nombres, 'apellido_p': apellido_p,
                    'apellido_m': apellido_m, 'email': email, 'sexo': sexo,
                    'telefono': telefono, 'estado_usuario_id': estado_usuario_id,
                    'rol_id': rol_id, 'membresia_id': membresia_id
                },
                **get_dropdown_data()
            }
            return render(request, 'users/user_form.html', context)

    # Gestionar para obtener los datos de la db, metodo GET
    try:
        query_search_user = """
            SELECT * FROM usuarios
            WHERE rut = %s;
        """

        user_found = db.get_one(query_search_user, (rut,))

        if not user_found:
            return redirect('users:user_list')
    except Exception as e:
        print(f"Error al buscar [Usuario]: {str(e)}")
        user_found = None

    context = {
        'usuario': user_found,
        **get_dropdown_data()
    }

    return render(request, 'users/user_form.html', context)


@role_required(['Admin'])
@login_required_manual
def admin_dashboard(request):
    db = DatabaseManager()
    context = {}

    try:
        # Total Usuarios Activos
        stats_usuarios = db.get_one(
            "SELECT COUNT(*) as total FROM usuarios WHERE is_active = 1")

        # Reservas del Mes (Canchas + Quinchos)
        query_reservas_mes = """
            SELECT
                (SELECT COUNT(*) FROM reservas_canchas WHERE MONTH(fecha) = MONTH(CURRENT_DATE) AND YEAR(fecha) = YEAR(CURRENT_DATE)) +
                (SELECT COUNT(*) FROM reservas_quinchos WHERE MONTH(fecha) = MONTH(CURRENT_DATE) AND YEAR(fecha) = YEAR(CURRENT_DATE)) as total
        """
        stats_reservas = db.get_one(query_reservas_mes)

        # Ingresos Totales (Reservas Pagadas + Multas Pagadas)
        query_ingresos = """
            SELECT
                (SELECT IFNULL(SUM(valor_pagado), 0) FROM reservas_canchas WHERE estado_id = 2) +
                (SELECT IFNULL(SUM(valor_pagado), 0) FROM reservas_quinchos WHERE estado_id = 2) +
                (SELECT IFNULL(SUM(monto_cobrado), 0) FROM usuarios_penalizaciones WHERE pagada = 1) as total
        """
        stats_ingresos = db.get_one(query_ingresos)

        # Penalizaciones Pendientes
        stats_penalizaciones = db.get_one(
            "SELECT COUNT(*) as total FROM usuarios_penalizaciones WHERE pagada = 0")

        context = {
            'total_usuarios': stats_usuarios['total'],
            'total_reservas': stats_reservas['total'],
            'total_ingresos': stats_ingresos['total'],
            'total_penalizaciones': stats_penalizaciones['total'],
        }
    except Exception as e:
        print(f"ERROR DB [Admin Dashboard]: {str(e)}")

    return render(request, 'users/dashboards/admin.html', context)


@role_required(['Recepcionista'])
@login_required_manual
def recepcionista_dashboard(request):
    db = DatabaseManager()
    context = {}
    try:
        # Consultar las próximas 5 reservas de HOY (Canchas + Quinchos)
        query_hoy = """
            SELECT * FROM (
                SELECT
                    rc.reserva_cancha_id as id, 'Cancha' as tipo, rc.fecha, rc.hora,
                    CONCAT(u.nombres, ' ', u.apellido_p) as cliente,
                    c.nombre as recurso, er.nombre as estado, er.estado_reserva_id
                FROM reservas_canchas rc
                JOIN usuarios u ON rc.usuario_rut = u.rut
                JOIN canchas c ON rc.cancha_id = c.cancha_id
                JOIN estados_reservas er ON rc.estado_id = er.estado_reserva_id
                WHERE rc.fecha = CURRENT_DATE AND rc.estado_id IN (1, 2)

                UNION ALL

                SELECT
                    rq.reserva_quincho_id as id, 'Quincho' as tipo, rq.fecha, rq.hora,
                    CONCAT(u.nombres, ' ', u.apellido_p) as cliente,
                    q.nombre as recurso, er.nombre as estado, er.estado_reserva_id
                FROM reservas_quinchos rq
                JOIN usuarios u ON rq.usuario_rut = u.rut
                JOIN quinchos q ON rq.quincho_id = q.quincho_id
                JOIN estados_reservas er ON rq.estado_id = er.estado_reserva_id
                WHERE rq.fecha = CURRENT_DATE AND rq.estado_id IN (1, 2)
            ) AS reservas_hoy
            ORDER BY hora ASC
            LIMIT 5
        """

        reservas_hoy = db.get_all(query_hoy)

        context = {
            'reservas_hoy': reservas_hoy
        }
    except Exception as e:
        print(f"ERROR DB [Recepcionista Dashboard]: {str(e)}")

    return render(request, 'users/dashboards/recepcionista.html', context)


@role_required(['Cliente'])
@login_required_manual
def cliente_dashboard(request):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    context = {}
    try:
        # Consultar la PRÓXIMA reserva (Cancha o Quincho) del usuario logueado
        query_proxima = """
            SELECT * FROM (
                SELECT
                    rc.reserva_cancha_id as id, 'Cancha' as tipo, rc.fecha, rc.hora,
                    c.nombre as recurso
                FROM reservas_canchas rc
                JOIN canchas c ON rc.cancha_id = c.cancha_id
                WHERE rc.usuario_rut = %s AND (rc.fecha > CURRENT_DATE OR (rc.fecha = CURRENT_DATE AND rc.hora >= CURRENT_TIME)) AND rc.estado_id IN (1, 2)

                UNION ALL

                SELECT
                    rq.reserva_quincho_id as id, 'Quincho' as tipo, rq.fecha, rq.hora,
                    q.nombre as recurso
                FROM reservas_quinchos rq
                JOIN quinchos q ON rq.quincho_id = q.quincho_id
                WHERE rq.usuario_rut = %s AND (rq.fecha > CURRENT_DATE OR (rq.fecha = CURRENT_DATE AND rq.hora >= CURRENT_TIME)) AND rq.estado_id IN (1, 2)
            ) AS proximas
            ORDER BY fecha ASC, hora ASC
            LIMIT 1
        """

        proxima_reserva = db.get_one(query_proxima, (user_rut, user_rut))

        context = {
            'proxima_reserva': proxima_reserva
        }
    except Exception as e:
        print(f"ERROR DB [Cliente Dashboard]: {str(e)}")

    return render(request, 'users/dashboards/cliente.html', context)


@login_required_manual
def profile(request):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    context = {}

    # Obtener datos actuales del usuario (para el GET y para validar pass en POST)
    try:
        query_user = """
            SELECT
                u.rut, u.nombres, u.apellido_p, u.apellido_m,
                u.email, u.telefono, u.password,
                r.nombre as rol, m.nombre as membresia
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.rol_id
            LEFT JOIN membresias m ON u.membresia_id = m.membresia_id
            WHERE u.rut = %s
        """
        user_found = db.get_one(query_user, (user_rut,))
        context = {
            'usuario': user_found
        }
    except Exception as e:
        print(f"ERROR DB [Cargar Perfil]: {str(e)}")

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # VALIDACIÓN 1: Email duplicado en otro usuario
        try:
            email_exists = db.get_one(
                "SELECT rut FROM usuarios WHERE email = %s AND rut != %s",
                (email, user_rut)
            )
            if email_exists:
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Error',
                        'message': 'Ese correo electrónico ya está en uso por otra cuenta.'
                    },
                    'usuario': user_found
                }
                return render(request, 'users/profile.html', context)
        except Exception as e:
            print(f"ERROR DB [Validar Email]: {str(e)}")

        # VALIDACIÓN 2: Si intenta cambiar password, validar campos
        if current_password or new_password or confirm_password:
            if not current_password or not new_password or not confirm_password:
                context = {
                    'sw_alert': {
                        'type': 'warning',
                        'title': 'Atención',
                        'message': 'Debe completar todos los campos de contraseña para cambiarla.'
                    },
                    'usuario': user_found
                }
                return render(request, 'users/profile.html', context)

            if new_password != confirm_password:
                context = {
                    'sw_alert': {
                        'type': 'warning',
                        'title': 'Atención',
                        'message': 'Las nuevas contraseñas no coinciden.'
                    },
                    'usuario': user_found
                }
                return render(request, 'users/profile.html', context)

            if not check_password(current_password, user_found['password']):
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Error',
                        'message': 'La contraseña actual es incorrecta.'
                    },
                    'usuario': user_found
                }
                return render(request, 'users/profile.html', context)

            # Actualizar con Password
            try:
                hashed_password = make_password(new_password)
                db.execute(
                    "UPDATE usuarios SET telefono = %s, email = %s, password = %s WHERE rut = %s",
                    (telefono, email, hashed_password, user_rut)
                )
            except Exception as e:
                print(f"ERROR DB [Update Perfil Pass]: {str(e)}")
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Error',
                        'message': 'No se pudo actualizar la contraseña.'
                    }
                }
                return render(request, 'users/profile.html', context)
        else:
            # ACTUALIZACIÓN 3: Solo datos básicos (sin password)
            try:
                db.execute(
                    "UPDATE usuarios SET telefono = %s, email = %s WHERE rut = %s",
                    (telefono, email, user_rut)
                )
            except Exception as e:
                print(f"ERROR DB [Update Perfil Base]: {str(e)}")
                context = {
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Error',
                        'message': 'No se pudieron actualizar los datos.'
                    }
                }
                return render(request, 'users/profile.html', context)

        # Actualizar sesión y mostrar mensaje
        request.session['user_email'] = email
        context = {
            'sw_alert': {
                'type': 'success',
                'title': 'Perfil Actualizado',
                'message': 'Tus datos han sido actualizados correctamente.',
                'redirect': reverse('users:profile')
            }
        }
        return render(request, 'users/profile.html', context)

    return render(request, 'users/profile.html', context)
