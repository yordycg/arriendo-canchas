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


@login_required_manual
@role_required(['Admin'])
def membership_create(request):
    db = DatabaseManager()
    context = {}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        porcentaje_descuento = int(request.POST.get('porcentaje_descuento', 0))
        costo_mensual = float(request.POST.get('costo_mensual', 0.0))

        try:
            query_add_membership = """
                INSERT INTO membresias (nombre, porcentaje_descuento, costo_mensual)
                VALUES (%s, %s, %s)
            """
            params = (nombre, porcentaje_descuento, costo_mensual)
            db.execute(query_add_membership, params)

            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Plan Registrado!',
                    'message': f'La membresía "{nombre}" ha sido creada exitosamente.',
                    'redirect': reverse('memberships:membership_list')
                }
            }
            return render(request, 'memberships/membership_form.html', context)
        except Exception as e:
            print(f"ERROR DB [Crear Membresía]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Registro',
                    'message': 'No se pudo crear el plan. Verifique que el nombre sea único.'
                }
            }
            return render(request, 'memberships/membership_form.html', context)

    return render(request, 'memberships/membership_form.html', context)
