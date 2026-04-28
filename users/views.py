from django.shortcuts import redirect, render
from django.http import HttpResponse
from .db import DatabaseManager

# Create your views here.


def home(request):
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
        LEFT JOIN membresias m ON u.membresia_id = m.membresia_id;
    """

    usuarios = db.get_all(query_all_usuarios)

    context = {
        'usuarios': usuarios
    }

    return render(request, 'users/home.html', context)


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


def add_user(request):
    if request.method == 'GET':
        # Obtener los datos del form...
        rut = request.GET.get('rut')
        nombres = request.GET.get('nombres')
        apellido_p = request.GET.get('apellido_p')
        apellido_m = request.GET.get('apellido_m')
        email = request.GET.get('email')
        password = request.GET.get('password')
        sexo = request.GET.get('sexo')
        telefono = request.GET.get('telefono')
        estado_usuario_id = int(request.GET.get('estado_usuario_id'))
        rol_id = int(request.GET.get('rol_id'))
        membresia_id = int(request.GET.get('membresia_id'))

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
        return redirect('/users/')
