from django.shortcuts import render, redirect
from django.urls import reverse
from database.db import DatabaseManager
from authentication.decorators import login_required_manual, role_required


@login_required_manual
def membership_list(request):
    db = DatabaseManager()
    context = {}

    try:
        query_all_membresias = """
            SELECT
                membresia_id,
                nombre,
                porcentaje_descuento,
                costo_mensual,
                is_active
            FROM membresias
            WHERE is_active = 1
        """
        memberships = db.get_all(query_all_membresias)

        context = {
            'membresias': memberships
        }
    except Exception as e:
        print(f"ERROR CRITICO DB [Membresías]: {str(e)}")
        context = {
            'sw_alert': {
                'type': 'error',
                'title': 'Error del Sistema',
                'message': 'No pudimos conectar con la base de datos para cargar los planes de membresía.',
            }
        }
    return render(request, 'memberships/membership_list.html', context)
