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


@login_required_manual
@role_required(['Admin'])
def court_create(request):
    db = DatabaseManager()
    context = {}

    tipos_canchas = db.get_all(
        "SELECT tipo_cancha_id, nombre FROM tipos_canchas WHERE is_active = 1")
    superficies = ['Pasto Sintetico', 'Pasto Natural',
                   'Arcilla', 'Cemento', 'Parquet', 'Baldosa']
    recintos = ['Abierto', 'Semi-techado', 'Cerrado']

    def get_dropdown_data():
        return {
            'tipos_canchas': tipos_canchas,
            'superficies': superficies,
            'recintos': recintos
        }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        valor_hora = request.POST.get('valor_hora')
        tipo_superficie = request.POST.get('tipo_superficie')
        tipo_recinto = request.POST.get('tipo_recinto')
        tipo_cancha_id = request.POST.get('tipo_cancha_id')

        try:
            query = """
                INSERT INTO canchas (nombre, valor_hora, tipo_superficie, tipo_recinto, tipo_cancha_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (nombre, valor_hora, tipo_superficie,
                      tipo_recinto, tipo_cancha_id)
            db.execute(query, params)

            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Cancha Creada!',
                    'message': f'La cancha "{nombre}" ha sido registrada exitosamente.',
                    'redirect': reverse('courts:court_list')
                }
            }
            return render(request, 'courts/court_form.html', context)

        except Exception as e:
            print(f"ERROR DB [Crear Cancha]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Registro',
                    'message': 'No se pudo crear la cancha. Verifique los datos.'
                },
                **get_dropdown_data()
            }
            return render(request, 'courts/court_form.html', context)

    return render(request, 'courts/court_form.html', get_dropdown_data())


@login_required_manual
@role_required(['Admin'])
def pavilion_create(request):
    db = DatabaseManager()
    context = {}

    estados = db.get_all(
        "SELECT estado_quincho_id, nombre FROM estados_quinchos")

    def get_dropdown_data():
        return {'estados': estados}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        valor_reserva = request.POST.get('valor_reserva')
        solo_vip = 1 if request.POST.get('solo_vip') == 'on' else 0
        estado_quincho_id = request.POST.get('estado_quincho_id')

        try:
            query = """
                INSERT INTO quinchos (nombre, valor_reserva, solo_vip, estado_quincho_id)
                VALUES (%s, %s, %s, %s)
            """
            params = (nombre, valor_reserva, solo_vip, estado_quincho_id)
            db.execute(query, params)

            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Quincho Creado!',
                    'message': f'El quincho "{nombre}" ha sido registrado exitosamente.',
                    'redirect': reverse('courts:court_list') + '?tab=pavilions'
                }
            }
            return render(request, 'courts/pavilion_form.html', context)

        except Exception as e:
            print(f"ERROR DB [Crear Quincho]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Registro',
                    'message': 'No se pudo crear el quincho. Verifique los datos.'
                },
                **get_dropdown_data()
            }
            return render(request, 'courts/pavilion_form.html', context)

    return render(request, 'courts/pavilion_form.html', get_dropdown_data())


@login_required_manual
@role_required(['Admin'])
def court_update(request, cancha_id):
    db = DatabaseManager()
    context = {}
    
    # Datos para selects
    tipos_canchas = db.get_all("SELECT tipo_cancha_id, nombre FROM tipos_canchas WHERE is_active = 1")
    superficies = ['Pasto Sintético', 'Pasto Natural', 'Arcilla', 'Cemento', 'Parquet', 'Baldosa']
    recintos = ['Abierto', 'Semi-techado', 'Cerrado']
    
    def get_dropdown_data():
        return {
            'tipos_canchas': tipos_canchas,
            'superficies': superficies,
            'recintos': recintos
        }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        valor_hora = request.POST.get('valor_hora')
        tipo_superficie = request.POST.get('tipo_superficie')
        tipo_recinto = request.POST.get('tipo_recinto')
        tipo_cancha_id = request.POST.get('tipo_cancha_id')
        
        try:
            query = """
                UPDATE canchas 
                SET nombre=%s, valor_hora=%s, tipo_superficie=%s, tipo_recinto=%s, tipo_cancha_id=%s
                WHERE cancha_id=%s
            """
            params = (nombre, valor_hora, tipo_superficie, tipo_recinto, tipo_cancha_id, cancha_id)
            db.execute(query, params)
            
            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Cancha Actualizada!',
                    'message': f'Los datos de la cancha "{nombre}" han sido guardados.',
                    'redirect': reverse('courts:court_list')
                }
            }
            return render(request, 'courts/court_form.html', context)
            
        except Exception as e:
            print(f"ERROR DB [Actualizar Cancha]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Actualización',
                    'message': 'No se pudieron guardar los cambios.'
                },
                'cancha': {
                    'cancha_id': cancha_id, 'nombre': nombre, 'valor_hora': valor_hora,
                    'tipo_superficie': tipo_superficie, 'tipo_recinto': tipo_recinto,
                    'tipo_cancha_id': int(tipo_cancha_id)
                },
                **get_dropdown_data()
            }
            return render(request, 'courts/court_form.html', context)

    # Metodo GET: Buscar datos actuales
    try:
        cancha = db.get_one("SELECT * FROM canchas WHERE cancha_id = %s", (cancha_id,))
        if not cancha:
            return redirect('courts:court_list')
    except Exception as e:
        print(f"Error al buscar cancha: {e}")
        return redirect('courts:court_list')

    context = {
        'cancha': cancha,
        **get_dropdown_data()
    }
    return render(request, 'courts/court_form.html', context)


@login_required_manual
@role_required(['Admin'])
def pavilion_update(request, quincho_id):
    db = DatabaseManager()
    context = {}
    
    estados = db.get_all("SELECT estado_quincho_id, nombre FROM estados_quinchos")
    
    def get_dropdown_data():
        return {'estados': estados}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        valor_reserva = request.POST.get('valor_reserva')
        solo_vip = 1 if request.POST.get('solo_vip') == 'on' else 0
        estado_quincho_id = request.POST.get('estado_quincho_id')
        
        try:
            query = """
                UPDATE quinchos 
                SET nombre=%s, valor_reserva=%s, solo_vip=%s, estado_quincho_id=%s
                WHERE quincho_id=%s
            """
            params = (nombre, valor_reserva, solo_vip, estado_quincho_id, quincho_id)
            db.execute(query, params)
            
            context = {
                'sw_alert': {
                    'type': 'success',
                    'title': '¡Quincho Actualizado!',
                    'message': f'Los datos del quincho "{nombre}" han sido guardados.',
                    'redirect': reverse('courts:court_list') + '?tab=pavilions'
                }
            }
            return render(request, 'courts/pavilion_form.html', context)
            
        except Exception as e:
            print(f"ERROR DB [Actualizar Quincho]: {str(e)}")
            context = {
                'sw_alert': {
                    'type': 'error',
                    'title': 'Error de Actualización',
                    'message': 'No se pudieron guardar los cambios.'
                },
                'quincho': {
                    'quincho_id': quincho_id, 'nombre': nombre, 
                    'valor_reserva': valor_reserva, 'solo_vip': solo_vip,
                    'estado_quincho_id': int(estado_quincho_id)
                },
                **get_dropdown_data()
            }
            return render(request, 'courts/pavilion_form.html', context)

    # Metodo GET: Buscar datos actuales
    try:
        quincho = db.get_one("SELECT * FROM quinchos WHERE quincho_id = %s", (quincho_id,))
        if not quincho:
            return redirect('courts:court_list')
    except Exception as e:
        print(f"Error al buscar quincho: {e}")
        return redirect('courts:court_list')

    context = {
        'quincho': quincho,
        **get_dropdown_data()
    }
    return render(request, 'courts/pavilion_form.html', context)


@login_required_manual
@role_required(['Admin'])
def court_delete(request, cancha_id):
    try:
        db = DatabaseManager()
        # Soft-delete: marcar como inactivo
        db.execute("UPDATE canchas SET is_active = 0 WHERE cancha_id = %s", (cancha_id,))
    except Exception as e:
        print(f"ERROR DB [Eliminar Cancha]: {str(e)}")
        
    return redirect('courts:court_list')


@login_required_manual
@role_required(['Admin'])
def pavilion_delete(request, quincho_id):
    try:
        db = DatabaseManager()
        # Soft-delete: marcar como inactivo
        db.execute("UPDATE quinchos SET is_active = 0 WHERE quincho_id = %s", (quincho_id,))
    except Exception as e:
        print(f"ERROR DB [Eliminar Quincho]: {str(e)}")
        
    return redirect(reverse('courts:court_list') + '?tab=pavilions')
