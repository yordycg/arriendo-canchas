from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual
from datetime import datetime, time, timedelta

# Create your views here.


@login_required_manual
def booking_list(request):
    db = DatabaseManager()
    context = {}
    user_rut = request.session.get('user_rut')
    user_rol = request.session.get('user_rol')

    try:
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


@login_required_manual
def booking_create(request):
    db = DatabaseManager()
    user_rut = request.session.get('user_rut')
    context = {'today': datetime.now().date()}

    # Cargar recursos
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
            # PASO A: Validación, bloqueo por faltas (>= 5)
            query_user = "SELECT contador_faltas, membresia_id FROM usuarios WHERE rut = %s"
            user_data = db.get_one(query_user, [user_rut])

            if user_data['contador_faltas'] >= 5:
                context.update({
                    'sw_alert': {
                        'type': 'error',
                        'title': 'Usuario Bloqueado',
                        'message': 'Tienes 5 o más faltas. No puedes reservar.'
                    },
                    **load_resources()
                })
                return render(request, 'bookings/booking_form.html', context)

            # PASO B: Validar el quincho VIP
            if tipo == 'Quincho':
                quincho = db.get_one(
                    "SELECT solo_vip FROM quinchos WHERE quincho_id = %s", [recurso_id])
                # 1 = Normal
                if quincho['solo_vip'] and (not user_data['membresia_id'] or user_data['membresia_id'] == 1):
                    context.update({
                        'sw_alert': {
                            'type': 'warning',
                            'title': 'Acceso Denegado',
                            'message': 'Este quincho es exclusivo para socios VIP.'
                        },
                        **load_resources()
                    })
                    return render(request, 'bookings/booking_form.html', context)

            # PASO C: Hacer una validación, una doble comprobación de 'disponibilidad' (para canchas, y quinchos)
            check_table = "reservas_canchas" if tipo == "Cancha" else "reservas_quinchos"
            check_col = "cancha_id" if tipo == "Cancha" else "quincho_id"
            query_check = f"SELECT 1 FROM {check_table} WHERE {check_col} = %s AND fecha = %s AND hora = %s AND estado_id != 3"

            if db.exists(query_check, [recurso_id, fecha, hora]):
                context.update({
                    'sw_alert': {
                        'type': 'error',
                        'title': 'No Disponible',
                        'message': 'Lo sentimos, este horario acaba de ser tomado.'
                    },
                    **load_resources()
                })
                return render(request, 'bookings/booking_form.html', context)

            # PASO D: Calcular precio
            # Obtener precio base
            if tipo == 'Cancha':
                res_info = db.get_one(
                    "SELECT valor_hora as precio FROM canchas WHERE cancha_id = %s", [recurso_id])
            else:
                res_info = db.get_one(
                    "SELECT valor_reserva as precio FROM quinchos WHERE quincho_id = %s", [recurso_id])

            # Obtener descuento membresía
            memb_info = db.get_one("""
                SELECT m.porcentaje_descuento
                FROM usuarios u
                LEFT JOIN membresias m ON u.membresia_id = m.membresia_id
                WHERE u.rut = %s
            """, [user_rut])

            descuento = memb_info['porcentaje_descuento'] if memb_info and memb_info['porcentaje_descuento'] else 0
            precio_final = float(res_info['precio']) * (1 - (descuento / 100))

            # PASO E: Insertar reserva
            query_insert = f"""
                INSERT INTO {check_table} (fecha, hora, hora_fin, valor_pagado, estado_id, {check_col}, usuario_rut)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Estado 1 = Pendiente (asumiendo que paga en el recinto o después)
            db.execute(query_insert, [
                       fecha, hora, hora_fin, precio_final, 1, recurso_id, user_rut])

            context.update({
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Reserva Exitosa!',
                    'message': f'Se ha reservado con éxito. Total a pagar: ${precio_final:,.0f}',
                    'redirect': reverse('bookings:booking_list')
                }
            })
            return render(request, 'bookings/booking_form.html', context)
        except Exception as e:
            print(f"ERROR DB [Crear Reserva]: {str(e)}")
            context.update({
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error',
                    'message': 'Ocurrió un error al procesar la reserva.'
                },
                **load_resources()
            })
            return render(request, 'bookings/booking_form.html', context)
    # GET
    try:
        context.update(load_resources())
    except Exception as e:
        print(f"ERROR DB [Cargar Recursos]: {str(e)}")

    return render(request, 'bookings/booking_form.html', context)


@login_required_manual
def get_available_blocks(request):
    """
    Endpoint AJAX para obtener bloques de 1 hora disponibles.
    """
    recurso_id = request.GET.get('recurso_id')
    tipo = request.GET.get('tipo')
    fecha = request.GET.get('fecha')

    if not all([recurso_id, tipo, fecha]):
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    db = DatabaseManager()

    HORA_APERTURA = 8
    HORA_CIERRE = 23

    # Obtener reservas existentes
    if tipo == 'Cancha':
        query = "SELECT hora, hora_fin FROM reservas_canchas WHERE cancha_id = %s AND fecha = %s AND estado_id != 3"
    else:
        query = "SELECT hora, hora_fin FROM reservas_quinchos WHERE quincho_id = %s AND fecha = %s AND estado_id != 3"

    try:
        reservas = db.get_all(query, [recurso_id, fecha])

        bloques = []
        for h in range(HORA_APERTURA, HORA_CIERRE):
            inicio_s = h * 3600
            fin_s = (h + 1) * 3600

            esta_ocupado = False
            for res in reservas:
                def to_seconds(t):
                    if isinstance(t, timedelta):
                        return t.total_seconds()
                    if isinstance(t, time):
                        return t.hour * 3600 + t.minute * 60
                    return 0

                rs_inicio = to_seconds(res['hora'])
                rs_fin = to_seconds(res['hora_fin'])

                if inicio_s < rs_fin and fin_s > rs_inicio:
                    esta_ocupado = True
                    break

            if not esta_ocupado:
                bloques.append({
                    'inicio': f"{h:02d}:00",
                    'fin': f"{(h+1):02d}:00"
                })

        return JsonResponse({'bloques': bloques})
    except Exception as e:
        print(f"ERROR AJAX [Disponibilidad]: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
