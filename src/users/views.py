from django.shortcuts import redirect, render
from django.http import HttpResponse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required

# Create your views here.


@login_required_manual
def user_list(request):
    db = DatabaseManager()

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

    usuarios = db.get_all(query_all_usuarios)

    context = {
        'usuarios': usuarios
    }

    return render(request, 'users/home.html', context)


@login_required_manual
def user_form(request):
    db = DatabaseManager()

    query_all_roles = 'SELECT rol_id, nombre FROM roles;'
    query_all_estados_usuarios = 'SELECT estado_usuario_id, nombre FROM estados_usuarios;'
    query_all_membresias = 'SELECT membresia_id, nombre FROM membresias;'

    roles = db.get_all(query_all_roles)
    estados_usuarios = db.get_all(query_all_estados_usuarios)
    membresias = db.get_all(query_all_membresias)

    context = {
        'roles': roles,
        'estados': estados_usuarios,
        'membresias': membresias
    }

    return render(request, 'users/user_form.html', context)


@login_required_manual
@role_required(['Administrador'])
def user_create(request):
    if request.method == 'POST':
        # Obtener los datos del form...
        rut = request.POST.get('rut')
        nombres = request.POST.get('nombres')
        apellido_p = request.POST.get('apellido_p')
        apellido_m = request.POST.get('apellido_m')
        email = request.POST.get('email')
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

        db = DatabaseManager()

        # Validar que no exista el 'rut' a ingresar
        query_validar_rut = 'SELECT * FROM usuarios WHERE rut = %s;'

        if db.exists(query_validar_rut, (rut,)):
            context = {
                'error': 'Error, ya existe un registro asociado a ese RUT.'
            }
            # TODO: OJO, cuando tenemos un rut duplicado igual redireccionamos!!
        else:
            query_add_user = """
                INSERT INTO usuarios
                (rut, nombres, apellido_p, apellido_m, email, password, sexo, telefono, estado_usuario_id, rol_id, membresia_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """
            params = (rut, nombres, apellido_p, apellido_m, email, password,
                      sexo, telefono, estado_usuario_id, rol_id, membresia_id)

            db.execute(query_add_user, params)

            context = {'success': 'Registro insertado correctamente'}

        # return render(request, 'users/user_form.html', context)
        return redirect('users:user_list')

@login_required_manual
@role_required(['Administrador'])
def user_delete(request):
    rut = request.GET.get('rut')

    db = DatabaseManager()

    # Tecnica SOFT-DELETE: marcar como inactivo
    query_delete = "UPDATE usuarios SET is_active = 0 WHERE rut = %s;"

    db.execute(query_delete, (rut,))

    return redirect('users:user_list')
