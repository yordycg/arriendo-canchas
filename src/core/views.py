from django.shortcuts import render
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required

# Create your views here.


@role_required(['Admin'])
@login_required_manual
def admin_view(request):
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

    return render(request, 'core/dashboards/admin.html', context)


@role_required(['Recepcionista'])
@login_required_manual
def recepcion_view(request):
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

    return render(request, 'core/dashboards/recepcionista.html', context)


@role_required(['Cliente'])
@login_required_manual
def cliente_view(request):
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

    return render(request, 'core/dashboards/cliente.html', context)
