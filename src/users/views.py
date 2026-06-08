from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
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
    return render(request, 'users/dashboards/admin.html')


@role_required(['Recepcionista'])
@login_required_manual
def recepcionista_dashboard(request):
    return render(request, 'users/dashboards/recepcionista.html')


@role_required(['Cliente'])
@login_required_manual
def cliente_dashboard(request):
    return render(request, 'users/dashboards/cliente.html')
