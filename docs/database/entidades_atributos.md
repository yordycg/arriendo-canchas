# Entidades y Atributos

Detalle técnico de todas las tablas en `arriendo_canchas_db`.

## estados_usuarios / estados_reservas / estados_quinchos / roles
*Tablas Maestras (Lookups)*
- **id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(30), UNIQUE, NOT NULL)
- **created_at / updated_at** (TIMESTAMP)

## membresias
- **membresia_id (PK)** (INT)
- **nombre** (VARCHAR(30), UNIQUE, NOT NULL) (Normal, VIP, Socio)
- **porcentaje_descuento** (INT, CHECK 0-100)
- **costo_mensual** (DECIMAL(12,2), CHECK >= 0)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## tipos_canchas
- **tipo_cancha_id (PK)** (INT)
- **nombre** (VARCHAR(50), UNIQUE, NOT NULL)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## canchas
- **cancha_id (PK)** (INT)
- **nombre** (VARCHAR(100), NOT NULL)
- **valor_hora** (DECIMAL(12,2), CHECK >= 0)
- **tipo_superficie** (VARCHAR(50), CHECK: Pasto Sintético, Pasto Natural, Arcilla, Cemento, Parquet, Baldosa)
- **tipo_recinto** (VARCHAR(50), CHECK: Abierto, Semi-techado, Cerrado)
- **tipo_cancha_id (FK)** (INT)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## usuarios
- **rut (PK)** (VARCHAR(12))
- **nombres** (VARCHAR(100))
- **apellido_p / apellido_m** (VARCHAR(100))
- **sexo** (CHAR(1), CHECK: M, F, O)
- **telefono** (VARCHAR(15))
- **email** (VARCHAR(150), UNIQUE, NULLABLE)
- **password** (VARCHAR(255), NULLABLE)
- **intentos_fallidos** (INT, DEFAULT 0)
- **contador_faltas** (INT, DEFAULT 0)
- **estado_usuario_id (FK)** (INT)
- **rol_id (FK)** (INT)
- **membresia_id (FK)** (INT, NULLABLE)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## quinchos
- **quincho_id (PK)** (INT)
- **nombre** (VARCHAR(100))
- **valor_reserva** (DECIMAL(12,2), CHECK >= 0)
- **solo_vip** (BOOLEAN)
- **estado_quincho_id (FK)** (INT)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## reservas_canchas / reservas_quinchos
- **id (PK)** (INT)
- **fecha** (DATE)
- **hora** (TIME)
- **valor_pagado** (DECIMAL(12,2), CHECK >= 0)
- **estado_id (FK)** (INT)
- **cancha_id / quincho_id (FK)** (INT)
- **usuario_rut (FK)** (VARCHAR(12))
- **created_at / updated_at** (TIMESTAMP)
- *RESTRICCIÓN:* UNIQUE (id_recurso, fecha, hora)

## equipos
- **equipo_id (PK)** (INT)
- **nombre** (VARCHAR(100))
- **capitan_id (FK -> usuarios.rut)** (VARCHAR(12))
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## equipos_usuarios
- **equipo_id (PK, FK)** (INT)
- **usuario_rut (PK, FK)** (VARCHAR(12))

## torneos
- **torneo_id (PK)** (INT)
- **nombre** (VARCHAR(100))
- **fecha_inicio / fecha_fin** (DATE, CHECK: fin >= inicio)
- **tipo_cancha_id (FK)** (INT)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## partidos
- **partido_id (PK)** (INT)
- **torneo_id (FK)** (INT)
- **equipo_1_id / equipo_2_id (FK)** (INT, CHECK: equipo_1 <> equipo_2)
- **reserva_cancha_id (FK)** (INT)
- **resultado_equipo_1 / resultado_equipo_2** (INT, CHECK >= 0)
- **es_walkover** (BOOLEAN)
- **equipo_perdedor_id (FK)** (INT, CHECK: debe ser equipo 1 o 2)
- **created_at / updated_at** (TIMESTAMP)
- *RESTRICCIÓN:* IF Walkover THEN Result 3-0/0-3.

## tipo_penalizaciones
- **tipo_penalizacion_id (PK)** (INT)
- **nombre** (VARCHAR(50), UNIQUE)
- **descripcion** (TEXT)
- **valor_multa** (DECIMAL(12,2), CHECK >= 0)
- **dias_bloqueo** (INT, CHECK >= 0)
- **is_active** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)

## usuarios_penalizaciones
- **usuario_penalizado_id (PK)** (INT)
- **usuario_rut (FK)** (VARCHAR(12))
- **tipo_penalizacion_id (FK)** (INT)
- **fecha** (DATE)
- **pagada** (BOOLEAN)
- **created_at / updated_at** (TIMESTAMP)
