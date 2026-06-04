from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual
from datetime import datetime, time, timedelta

# Create your views here.


def get_bookings_data(request):
    """
    Función auxiliar para obtener las reservas según el rol.
    Evita duplicar la query en el listado y en la cancelación.
    """
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    user_rol = request.session.get('user_rol')

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

    if user_rol not in ['Admin', 'Recepcionista']:
        where_clause = "WHERE rc.usuario_rut = %s"
        where_clause_q = "WHERE rq.usuario_rut = %s"
        params = [user_rut, user_rut]

    final_query = query_base.format(
        where_clause=where_clause, where_clause_q=where_clause_q)
    return db.get_all(final_query, params)


@login_required_manual
def booking_list(request):
    context = {}
    try:
        bookings = get_bookings_data(request)
        context = {'reservas': bookings}
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


@login_required_manual
def booking_create(request):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    context = {'today': datetime.now().date()}

    def load_resources():
        canchas = db.get_all(
            "SELECT cancha_id as id, nombre, valor_hora as precio, 'Cancha' as tipo FROM canchas WHERE is_active = 1")
        quinchos = db.get_all(
            "SELECT quincho_id as id, nombre, valor_reserva as precio, 'Quincho' as tipo, solo_vip FROM quinchos WHERE is_active = 1")
        return {'canchas': canchas, 'quinchos': quinchos}

    if request.method == 'POST':
        recurso_id = request.POST.get('recurso_id')
        tipo = request.POST.get('tipo')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        hora_fin = request.POST.get('hora_fin')

        try:
            # PASO A: Validación faltas
            user_data = db.get_one(
                "SELECT contador_faltas, membresia_id FROM usuarios WHERE rut = %s", [user_rut])

            if user_data['contador_faltas'] >= 5:
                context.update({
                    'sw_alert': {'type': 'error', 'title': 'Usuario Bloqueado', 'message': 'Tienes 5 o más faltas.'},
                    **load_resources()
                })
                return render(request, 'bookings/booking_form.html', context)

            # PASO B: Validar VIP
            if tipo == 'Quincho':
                quincho = db.get_one(
                    "SELECT solo_vip FROM quinchos WHERE quincho_id = %s", [recurso_id])
                if quincho['solo_vip'] and (not user_data['membresia_id'] or user_data['membresia_id'] == 1):
                    context.update({
                        'sw_alert': {'type': 'warning', 'title': 'Solo VIP', 'message': 'Este quincho es exclusivo.'},
                        **load_resources()
                    })
                    return render(request, 'bookings/booking_form.html', context)

            # PASO C: Disponibilidad
            check_table = "reservas_canchas" if tipo == "Cancha" else "reservas_quinchos"
            check_col = "cancha_id" if tipo == "Cancha" else "quincho_id"
            if db.exists(f"SELECT 1 FROM {check_table} WHERE {check_col} = %s AND fecha = %s AND hora = %s AND estado_id != 3", [recurso_id, fecha, hora]):
                context.update({
                    'sw_alert': {'type': 'error', 'title': 'No Disponible', 'message': 'El horario ya fue tomado.'},
                    **load_resources()
                })
                return render(request, 'bookings/booking_form.html', context)

            # PASO D: Precio
            res_query = "SELECT valor_hora as precio FROM canchas WHERE cancha_id = %s" if tipo == 'Cancha' else "SELECT valor_reserva as precio FROM quinchos WHERE quincho_id = %s"
            res_info = db.get_one(res_query, [recurso_id])
            memb_info = db.get_one(
                "SELECT COALESCE(m.porcentaje_descuento, 0) as descuento FROM usuarios u LEFT JOIN membresias m ON u.membresia_id = m.membresia_id WHERE u.rut = %s", [user_rut])

            precio_final = float(res_info['precio']) * \
                (1 - (memb_info['descuento'] / 100))

            # PASO E: Insertar
            query_insert = f"INSERT INTO {check_table} (fecha, hora, hora_fin, valor_pagado, estado_id, {check_col}, usuario_rut) VALUES (%s, %s, %s, %s, 1, %s, %s)"
            db.execute(query_insert, [fecha, hora, hora_fin,
                       precio_final, recurso_id, user_rut])

            context.update({
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Reserva Exitosa!',
                    'message': f'Total a pagar: ${precio_final:,.0f}',
                    'redirect': reverse('bookings:booking_list')
                }
            })
            return render(request, 'bookings/booking_form.html', context)

        except Exception as e:
            print(f"ERROR DB [Crear Reserva]: {str(e)}")
            context.update({
                'sw_alert': {'type': 'error', 'title': 'Error', 'message': 'No se pudo procesar.'},
                **load_resources()
            })
            return render(request, 'bookings/booking_form.html', context)

    context.update(load_resources())
    return render(request, 'bookings/booking_form.html', context)


@login_required_manual
def booking_cancel(request, tipo, id):
    """
    Cancela una reserva aplicando la regla de los 30 minutos.
    Sigue el patrón de alertas de users/ (render con redirect en sw_alert).
    """
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    user_rol = request.session.get('user_rol')
    context = {}

    table = "reservas_canchas" if tipo == "Cancha" else "reservas_quinchos"
    pk_col = "reserva_cancha_id" if tipo == "Cancha" else "reserva_quincho_id"

    try:
        # Obtener la reserva
        res = db.get_one(f"SELECT * FROM {table} WHERE {pk_col} = %s", [id])
        if not res or (res['usuario_rut'] != user_rut and user_rol not in ['Admin', 'Recepcionista']):
            return redirect('bookings:booking_list')

        # Calcular el tiempo
        res_hora = res['hora']
        if isinstance(res_hora, timedelta):
            res_hora = (datetime.min + res_hora).time()
        res_datetime = datetime.combine(res['fecha'], res_hora)
        minutos_faltantes = (res_datetime - datetime.now()
                             ).total_seconds() / 60

        # 3. Transacción
        # Transacción para cancelar
        # with: nos garantiza que pase lo que pase (bien o mal) dentro de un bloque de código
        # se ejecuta una rutina de limpieza al salir de este.
        with db.transaction() as cursor:
            cursor.execute(
                f"UPDATE {table} SET estado_id = 3 WHERE {pk_col} = %s", [id])
            if minutos_faltantes < 30:
                cursor.execute(
                    "UPDATE usuarios SET contador_faltas = contador_faltas + 1 WHERE rut = %s", [res['usuario_rut']])
                cursor.execute(
                    "INSERT INTO usuarios_penalizaciones (usuario_rut, tipo_penalizacion_id, fecha, pagada) VALUES (%s, 2, %s, 0)", [res['usuario_rut'], datetime.now().date()])
                msg = "Reserva cancelada con penalización por falta de anticipación."
            else:
                msg = "Reserva cancelada exitosamente."

        context = {
            'reservas': get_bookings_data(request),
            'sw_alert': {
                'type': 'success',
                'title': 'Cancelación',
                'message': msg,
                'redirect': reverse('bookings:booking_list')
            }
        }
        return render(request, 'bookings/booking_list.html', context)

    except Exception as e:
        print(f"ERROR DB [Cancelar Reserva]: {str(e)}")
        context = {
            'reservas': get_bookings_data(request),
            'sw_alert': {
                'type': 'error',
                'title': 'Error',
                'message': 'No se pudo cancelar.'
            }
        }
        return render(request, 'bookings/booking_list.html', context)


@login_required_manual
def get_available_blocks(request):
    recurso_id = request.GET.get('recurso_id')
    tipo = request.GET.get('tipo')
    fecha = request.GET.get('fecha')
    if not all([recurso_id, tipo, fecha]):
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    db = DatabaseManager()
    query = "SELECT hora, hora_fin FROM " + ("reservas_canchas" if tipo == 'Cancha' else "reservas_quinchos") + \
            " WHERE " + ("cancha_id" if tipo == 'Cancha' else "quincho_id") + \
            " = %s AND fecha = %s AND estado_id != 3"

    try:
        reservas = db.get_all(query, [recurso_id, fecha])
        bloques = []
        for h in range(8, 23):
            inicio_s, fin_s = h * 3600, (h + 1) * 3600
            esta_ocupado = False
            for res in reservas:
                def to_sec(t): return t.total_seconds() if isinstance(
                    t, timedelta) else (t.hour * 3600 + t.minute * 60 if isinstance(t, time) else 0)
                if inicio_s < to_sec(res['hora_fin']) and fin_s > to_sec(res['hora']):
                    esta_ocupado = True
                    break
            if not esta_ocupado:
                bloques.append(
                    {'inicio': f"{h:02d}:00", 'fin': f"{(h+1):02d}:00"})
        return JsonResponse({'bloques': bloques})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
