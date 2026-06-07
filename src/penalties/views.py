from django.shortcuts import render, redirect
from django.urls import reverse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required


@login_required_manual
@role_required(['Admin', 'Recepcionista'])
def penalty_list(request):
    db = DatabaseManager()
    context = {}

    try:
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
        penalties = db.get_all(query)
        context = {
            'penalizaciones': penalties
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
def penalty_pay(request, penalty_id):
    db = DatabaseManager()
    try:
        query_pay_penalty = """
            UPDATE usuarios_penalizaciones SET pagada = 1 WHERE usuario_penalizado_id = %s
        """
        db.execute(query_pay_penalty, (penalty_id,))

        # Opcional: Si el usuario ya no tiene deudas pendientes, podríamos actualizar su estado
        # Pero eso depende de las reglas de negocio específicas.

        return redirect('penalties:penalty_list')
    except Exception as e:
        print(f"ERROR DB [Pagar Penalizacion]: {str(e)}")
        return redirect('penalties:penalty_list')


@login_required_manual
@role_required(['Admin'])
def penalty_delete(request, penalty_id):
    db = DatabaseManager()
    try:
        query_delete_penalty = """
            DELETE FROM usuarios_penalizaciones WHERE usuario_penalizado_id = %s
        """

        db.execute(query_delete_penalty, (penalty_id,))
        return redirect('penalties:penalty_list')
    except Exception as e:
        print(f"ERROR DB [Eliminar Penalización]: {str(e)}")
        return redirect('penalties:penalty_list')


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
