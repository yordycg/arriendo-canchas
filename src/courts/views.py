from django.shortcuts import render, redirect
from django.urls import reverse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required


@login_required_manual
def court_list(request):
    db = DatabaseManager()
    context = {}

    try:
        query_all_canchas = """
            SELECT
                c.cancha_id,
                c.nombre,
                c.valor_hora,
                c.tipo_superficie,
                c.tipo_recinto,
                tc.nombre as tipo_cancha
            FROM canchas c
            JOIN tipos_canchas tc ON c.tipo_cancha_id = tc.tipo_cancha_id
            WHERE c.is_active = 1
        """
        courts = db.get_all(query_all_canchas)

        query_all_quinchos = """
            SELECT
                q.quincho_id,
                q.nombre,
                q.valor_reserva,
                q.solo_vip,
                eq.nombre as estado
            FROM quinchos q
            JOIN estados_quinchos eq ON q.estado_quincho_id = eq.estado_quincho_id
            WHERE q.is_active = 1
        """
        pavilions = db.get_all(query_all_quinchos)

        context = {
            'canchas': courts,
            'quinchos': pavilions
        }

    except Exception as e:
        print(f"ERROR CRITICO DB [Canchas/Quinchos]: {str(e)}")
        context = {
            'sw_alert': {
                'type': 'error',
                'title': 'Error del Sistema',
                'message': 'No pudimos conectar con la base de datos para cargar la infraestructura.',
            }
        }

    return render(request, 'courts/court_list.html', context)
