from django.shortcuts import render, redirect
from django.urls import reverse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required


def get_penalties_data():
    db = DatabaseManager()
    query = """
        SELECT
            up.usuario_penalizado_id,
            u.rut,
            CONCAT(u.nombres, ' ', u.apellido_p) as nombre_usuario,
            tp.nombre as tipo_penalizacion,
            tp.valor_multa,
            up.fecha,
            up.pagada
        FROM usuarios_penalizaciones up
        JOIN usuarios u ON up.usuario_rut = u.rut
        JOIN tipos_penalizaciones tp ON up.tipo_penalizacion_id = tp.tipo_penalizacion_id
        ORDER BY up.fecha DESC
    """
    return db.get_all(query)


@login_required_manual
@role_required(['Admin', 'Recepcionista'])
def penalty_list(request):
    context = {}
    try:
        context = {
            'penalizaciones': get_penalties_data()
        }
    except Exception as e:
        print(f"ERROR DB [Lista Penalizaciones]: {str(e)}")
        context = {
            'sw_alert': {
                'type': 'error',
                'title': 'Error',
                'message': 'No se pudo cargar el listado de penalizaciones.'
            }
        }
    return render(request, 'penalties/penalty_list.html', context)


@login_required_manual
@role_required(['Admin', 'Recepcionista'])
def penalty_create(request):
    db = DatabaseManager()
    context = {}

    if request.method == 'POST':
        usuario_rut = request.POST.get('usuario_rut')
        tipo_id = request.POST.get('tipo_penalizacion_id')
        fecha = request.POST.get('fecha')

        try:
            with db.transaction() as cursor:
                # Insertar la penalización
                cursor.execute(
                    "INSERT INTO usuarios_penalizaciones (usuario_rut, tipo_penalizacion_id, fecha, pagada) VALUES (%s, %s, %s, 0)",
                    [usuario_rut, tipo_id, fecha]
                )
                # Incrementar el contador de faltas del usuario
                cursor.execute(
                    "UPDATE usuarios SET contador_faltas = contador_faltas + 1 WHERE rut = %s",
                    [usuario_rut]
                )

            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': 'Penalización Creada',
                    'message': 'La penalización ha sido registrada y se sumó al contador del usuario.',
                    'redirect': reverse('penalties:penalty_list')
                }
            }
            return render(request, 'penalties/penalty_form.html', context)
        except Exception as e:
            print(f"ERROR DB [Crear Penalización]: {str(e)}")
            context['sw_alert'] = {
                'type': 'error',
                'title': 'Error',
                'message': 'No se pudo crear la penalización.'
            }

    try:
        # Solo los clientes pueden recibir penalizaciones
        query_usuarios = """
            SELECT u.rut, CONCAT(u.nombres, ' ', u.apellido_p, ' ', IFNULL(u.apellido_m, '')) as nombre 
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.rol_id
            WHERE u.is_active = 1 AND r.nombre = 'Cliente'
        """
        context['usuarios'] = db.get_all(query_usuarios)
        context['tipos'] = db.get_all("SELECT tipo_penalizacion_id, nombre, valor_multa FROM tipos_penalizaciones")
    except Exception as e:
        print(f"ERROR DB [Cargar Datos Form Penalización]: {str(e)}")

    return render(request, 'penalties/penalty_form.html', context)


@login_required_manual
def penalty_pay(request, penalty_id):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    user_rol = request.session.get('user_rol')
    context = {}

    try:
        # Verificar permisos y propiedad
        penalty_info = db.get_one("SELECT usuario_rut FROM usuarios_penalizaciones WHERE usuario_penalizado_id = %s", [penalty_id])
        if not penalty_info:
            return redirect('penalties:penalty_list' if user_rol in ['Admin', 'Recepcionista'] else 'penalties:my_penalties')

        if user_rol not in ['Admin', 'Recepcionista'] and penalty_info['usuario_rut'] != user_rut:
            # Si es cliente pero la multa no es suya
            return redirect('penalties:my_penalties')

        # Registrar el pago
        query_pay_penalty = """
            UPDATE usuarios_penalizaciones SET pagada = 1 WHERE usuario_penalizado_id = %s
        """
        db.execute(query_pay_penalty, (penalty_id,))

        is_staff = user_rol in ['Admin', 'Recepcionista']
        redirect_url = reverse('penalties:penalty_list') if is_staff else reverse('penalties:my_penalties')
        
        context = {
            'penalizaciones': get_penalties_data() if is_staff else db.get_all("""
                SELECT up.usuario_penalizado_id, tp.nombre as tipo_penalizacion, tp.valor_multa, up.fecha, up.pagada
                FROM usuarios_penalizaciones up
                JOIN tipos_penalizaciones tp ON up.tipo_penalizacion_id = tp.tipo_penalizacion_id
                WHERE up.usuario_rut = %s ORDER BY up.fecha DESC
            """, [user_rut]),
            'sw_alert': {
                'type': 'success',
                'title': 'Pago Registrado',
                'message': 'El pago de la multa se ha registrado correctamente.',
                'redirect': redirect_url
            }
        }
        
        template = 'penalties/penalty_list.html' if is_staff else 'penalties/my_penalties.html'
        return render(request, template, context)
        
    except Exception as e:
        print(f"ERROR DB [Pagar Penalizacion]: {str(e)}")
        is_staff = user_rol in ['Admin', 'Recepcionista']
        context = {
            'penalizaciones': get_penalties_data() if is_staff else db.get_all("""
                SELECT up.usuario_penalizado_id, tp.nombre as tipo_penalizacion, tp.valor_multa, up.fecha, up.pagada
                FROM usuarios_penalizaciones up
                JOIN tipos_penalizaciones tp ON up.tipo_penalizacion_id = tp.tipo_penalizacion_id
                WHERE up.usuario_rut = %s ORDER BY up.fecha DESC
            """, [user_rut]),
            'sw_alert': {
                'type': 'error',
                'title': 'Error',
                'message': 'No se pudo registrar el pago.'
            }
        }
        template = 'penalties/penalty_list.html' if is_staff else 'penalties/my_penalties.html'
        return render(request, template, context)


@login_required_manual
@role_required(['Admin'])
def penalty_delete(request, penalty_id):
    db = DatabaseManager()
    context = {}
    try:
        # Obtener el RUT del usuario para descontar la falta
        rut_result = db.get_one("SELECT usuario_rut FROM usuarios_penalizaciones WHERE usuario_penalizado_id = %s", [penalty_id])
        
        with db.transaction() as cursor:
            cursor.execute("DELETE FROM usuarios_penalizaciones WHERE usuario_penalizado_id = %s", [penalty_id])
            if rut_result:
                cursor.execute(
                    "UPDATE usuarios SET contador_faltas = GREATEST(0, contador_faltas - 1) WHERE rut = %s", 
                    [rut_result['usuario_rut']]
                )

        context = {
            'penalizaciones': get_penalties_data(),
            'sw_alert': {
                'type': 'success',
                'title': 'Penalización Eliminada',
                'message': 'La penalización fue eliminada y se descontó una falta al usuario.',
                'redirect': reverse('penalties:penalty_list')
            }
        }
    except Exception as e:
        print(f"ERROR DB [Eliminar Penalización]: {str(e)}")
        context = {
            'penalizaciones': get_penalties_data(),
            'sw_alert': {
                'type': 'error',
                'title': 'Error',
                'message': 'No se pudo eliminar la penalización.'
            }
        }
    return render(request, 'penalties/penalty_list.html', context)


@login_required_manual
def my_penalties(request):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    context = {}

    try:
        query = """
            SELECT
                up.usuario_penalizado_id,
                tp.nombre as tipo_penalizacion,
                tp.valor_multa,
                up.fecha,
                up.pagada
            FROM usuarios_penalizaciones up
            JOIN tipos_penalizaciones tp ON up.tipo_penalizacion_id = tp.tipo_penalizacion_id
            WHERE up.usuario_rut = %s
            ORDER BY up.fecha DESC
        """
        penalties = db.get_all(query, (user_rut,))
        context = {
            'penalizaciones': penalties
        }
    except Exception as e:
        print(f"ERROR DB [Mis Penalizaciones]: {str(e)}")

    return render(request, 'penalties/my_penalties.html', context)
