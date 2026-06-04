from django.shortcuts import render
from database.db import DatabaseManager
from authentication.decorators import login_required_manual

# Create your views here.


@login_required_manual
def booking_list(request):
    db = DatabaseManager()
    context = {}
    user_rut = request.session.get('user_rut')
    user_rol = request.session.get('user_rol')

    try:
        """
        Query básica donde usamos:
        - UNION ALL: nos permite "pegar" el resultado de una segunda query al lado del
        resultado de la primera query, y asi obtener una sola gran tabla.
        Se debe cumplir una regla, que ambas query deben tener el mismo numero
        de columnas y en el mismo orden.
        - {where_clause} (F-Strings y formateo): técnica de python aplicada a SQL, usamos
        un 'placeholder' (marcador de posición), en este caso si el usuario es 'Admin'
        el WHERE lo dejamos vació, pero si el usuario es 'Cliente' debemos mostrar solo
        lo relacionado a este (su RUT).
        """
        query_base = """
            SELECT
                'Cancha' as tipo,
                rc.reserva_cancha_id as id,
                rc.fecha,
                rc.hora,
                rc.hora_fin,
                rc.valor_pagado,
                er.nombre as estado,
                c.nombre as recurso,
                u.nombres,
                u.apellido_p,
                u.rut as usuario_rut
            FROM reservas_canchas rc
            JOIN canchas c ON rc.cancha_id = c.cancha_id
            JOIN estados_reservas er ON rc.estado_id = er.estado_reserva_id
            JOIN usuarios u ON rc.usuario_rut = u.rut
            {where_clause}
            UNION ALL
            SELECT
                'Quincho' as tipo,
                rq.reserva_quincho_id as id,
                rq.fecha,
                rq.hora,
                rq.hora_fin,
                rq.valor_pagado,
                er.nombre as estado,
                q.nombre as recurso,
                u.nombres,
                u.apellido_p,
                u.rut as usuario_rut
            FROM reservas_quinchos rq
            JOIN quinchos q ON rq.quincho_id = q.quincho_id
            JOIN estados_reservas er ON rq.estado_id = er.estado_reserva_id
            JOIN usuarios u ON rq.usuario_rut = u.rut
            {where_clause_q}
            ORDER BY fecha DESC, hora DESC;
        """

        params = []
        where_clause = ""
        where_clause_q = ""

        # Si no es Admin o Recepcionista, solo ve sus propias reservas
        if user_rol not in ['Admin', 'Recepcionista']:
            where_clause = "WHERE rc.usuario_rut = %s"
            where_clause_q = "WHERE rq.usuario_rut = %s"
            params = [user_rut, user_rut]

        final_query = query_base.format(
            where_clause=where_clause, where_clause_q=where_clause_q)
        bookings = db.get_all(final_query, params)

        context = {
            'reservas': bookings
        }
        return render(request, 'bookings/booking_list.html', context)

    except Exception as e:
        print(f"ERROR CRITICO DB [Reservas]: {str(e)}")
        context = {
            'sw_alert': {
                'type': 'error',
                'title': 'Error del Sistema',
                'message': 'No pudimos obtener el listado de reservas.',
            }
        }
        return render(request, 'bookings/booking_list.html', context)
