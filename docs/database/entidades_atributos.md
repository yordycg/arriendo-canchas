# Entidades y Atributos

Detalle técnico de todas las tablas en `arriendo_canchas_db`.

## estados_usuarios / estados_reservas / estados_quinchos / roles

_Tablas Maestras (Lookups)_

- **[nombre_tabla]_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(30), UNIQUE, NOT NULL)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## membresias

- **membresia_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(30), UNIQUE, NOT NULL) (Normal, VIP, Socio)
- **porcentaje_descuento** (INT, DEFAULT: 0, CHECK 0-100)
- **costo_mensual** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## tipos_canchas

- **tipo_cancha_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(50), UNIQUE, NOT NULL)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## canchas

- **cancha_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(100), NOT NULL)
- **valor_hora** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **tipo_superficie** (VARCHAR(50), CHECK: Pasto Sintetico, Pasto Natural, Arcilla, Cemento, Parquet, Baldosa)
- **tipo_recinto** (VARCHAR(50), CHECK: Abierto, Semi-techado, Cerrado)
- **tipo_cancha_id (FK)** (INT)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## usuarios

- **rut (PK)** (VARCHAR(12))
- **nombres** (VARCHAR(100), NOT NULL)
- **apellido_p / apellido_m** (VARCHAR(100))
- **sexo** (CHAR(1), DEFAULT: 'O', CHECK: M, F, O)
- **telefono** (VARCHAR(15))
- **email** (VARCHAR(150), UNIQUE)
- **password** (VARCHAR(255))
- **intentos_fallidos** (INT, DEFAULT 0)
- **contador_faltas** (INT, DEFAULT 0)
- **estado_usuario_id (FK)** (INT, DEFAULT: 1)
- **rol_id (FK)** (INT, DEFAULT: 3)
- **membresia_id (FK)** (INT, NULL)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## quinchos

- **quincho_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(100), NOT NULL)
- **valor_reserva** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **solo_vip** (BOOLEAN, DEFAULT: FALSE)
- **estado_quincho_id (FK)** (INT, DEFAULT: 1)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## reservas_canchas

- **reserva_cancha_id (PK)** (INT, AutoIncrement)
- **fecha** (DATE, NOT NULL)
- **hora** (TIME, NOT NULL)
- **hora_fin** (TIME, NOT NULL)
- **valor_pagado** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **estado_id (FK)** (INT, DEFAULT: 1)
- **cancha_id (FK)** (INT)
- **usuario_rut (FK)** (VARCHAR(12))
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- _RESTRICCIÓN:_ UNIQUE (cancha_id, fecha, hora)
- _RESTRICCIÓN:_ CHECK (hora_fin > hora)

## reservas_quinchos

- **reserva_quincho_id (PK)** (INT, AutoIncrement)
- **fecha** (DATE, NOT NULL)
- **hora** (TIME, NOT NULL)
- **hora_fin** (TIME, NOT NULL)
- **valor_pagado** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **estado_id (FK)** (INT, DEFAULT: 1)
- **quincho_id (FK)** (INT)
- **usuario_rut (FK)** (VARCHAR(12))
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- _RESTRICCIÓN:_ UNIQUE (quincho_id, fecha, hora)
- _RESTRICCIÓN:_ CHECK (hora_fin > hora)

## equipos

- **equipo_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(100), NOT NULL)
- **capitan_id (FK -> usuarios.rut)** (VARCHAR(12))
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## equipos_usuarios

- **equipo_id (PK, FK)** (INT)
- **usuario_rut (PK, FK)** (VARCHAR(12))
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## torneos

- **torneo_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(100), NOT NULL)
- **fecha_inicio / fecha_fin** (DATE, NOT NULL, CHECK: fin >= inicio)
- **tipo_cancha_id (FK)** (INT)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## partidos

- **partido_id (PK)** (INT, AutoIncrement)
- **torneo_id (FK)** (INT)
- **equipo_1_id / equipo_2_id (FK)** (INT, CHECK: equipo_1 <> equipo_2)
- **reserva_cancha_id (FK)** (INT)
- **resultado_equipo_1 / resultado_equipo_2** (INT, DEFAULT: 0, CHECK >= 0)
- **es_walkover** (BOOLEAN, DEFAULT: FALSE)
- **equipo_perdedor_id (FK)** (INT, CHECK: debe ser equipo 1 o 2)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- _RESTRICCIÓN:_ CHECK (es_walkover = FALSE OR (resultado_equipo_1 = 3 AND resultado_equipo_2 = 0) OR (resultado_equipo_1 = 0 AND resultado_equipo_2 = 3))

## tipos_penalizaciones

- **tipo_penalizacion_id (PK)** (INT, AutoIncrement)
- **nombre** (VARCHAR(50), UNIQUE, NOT NULL)
- **descripcion** (TEXT)
- **valor_multa** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **dias_bloqueo** (INT, DEFAULT: 0, CHECK >= 0)
- **is_active** (BOOLEAN, DEFAULT: TRUE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## usuarios_penalizaciones

- **usuario_penalizado_id (PK)** (INT, AutoIncrement)
- **usuario_rut (FK)** (VARCHAR(12))
- **tipo_penalizacion_id (FK)** (INT)
- **monto_cobrado** (DECIMAL(12,2), DEFAULT: 0.00, CHECK >= 0)
- **fecha** (DATE, DEFAULT: CURRENT_DATE)
- **pagada** (BOOLEAN, DEFAULT: FALSE)
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **updated_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

## auditoria_login

- **auditoria_id (PK)** (INT, AutoIncrement)
- **usuario** (VARCHAR(150), NOT NULL) (RUT o Email ingresado)
- **fecha_hora** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
- **estado_login** (VARCHAR(20), NOT NULL, CHECK: Correcto, Incorrecto)
- **password_ingresada** (VARCHAR(255), NULL) (Solo se registra si el estado es 'Incorrecto')
- **created_at** (TIMESTAMP, DEFAULT: CURRENT_TIMESTAMP)
