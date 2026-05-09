-- DATOS DE PRUEBA (Solo para desarrollo y testing)
USE arriendo_canchas_db;

-- Usuarios (Admin, VIP, Socio, Invitado)
INSERT INTO usuarios (rut, nombres, apellido_p, sexo, email, password, estado_usuario_id, rol_id, membresia_id) VALUES
('11.111.111-1', 'Admin', 'Sistema', 'M', 'admin@canchas.cl', 'pbkdf2_sha256$1200000$mWXtlqjGMJxFRgegXHz7G6$YD5sf87t7AMvX6WW66cp9njhZe7IT6In2WnnWVxJkp4=', 1, 1, NULL),
('22.222.222-2', 'Juan', 'Perez', 'M', 'juan@gmail.com', 'pbkdf2_sha256$1200000$mWXtlqjGMJxFRgegXHz7G6$YD5sf87t7AMvX6WW66cp9njhZe7IT6In2WnnWVxJkp4=', 1, 3, 2),
('33.333.333-3', 'Maria', 'Soto', 'F', 'maria@outlook.com', 'pbkdf2_sha256$1200000$mWXtlqjGMJxFRgegXHz7G6$YD5sf87t7AMvX6WW66cp9njhZe7IT6In2WnnWVxJkp4=', 1, 3, 3),
('44.444.444-4', 'Pedro', 'Invitado', 'M', NULL, NULL, 1, 4, 1); -- Usuario invitado para torneos

-- Canchas
INSERT INTO canchas (nombre, valor_hora, tipo_superficie, tipo_recinto, tipo_cancha_id) VALUES
('Maracaná 5', 25000.00, 'Pasto Sintético', 'Abierto', 1),
('Wimbledon Central', 15000.00, 'Pasto Natural', 'Abierto', 4),
('Estadio 7', 35000.00, 'Pasto Sintético', 'Cerrado', 2),
('Gimnasio Techado', 20000.00, 'Parquet', 'Cerrado', 6);

-- Quinchos
INSERT INTO quinchos (nombre, valor_reserva, solo_vip, estado_quincho_id) VALUES
('Quincho Familiar 1', 10000.00, FALSE, 1),
('Quincho VIP Premium', 25000.00, TRUE, 1);

-- Equipos
INSERT INTO equipos (nombre, capitan_id) VALUES
('Los Galácticos', '22.222.222-2'),
('Dream Team FC', '33.333.333-3');

-- Torneo
INSERT INTO torneos (nombre, fecha_inicio, fecha_fin, tipo_cancha_id) VALUES
('Liga Relámpago Verano', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 1);

-- Reservas de Canchas
INSERT INTO reservas_canchas (fecha, hora, valor_pagado, estado_id, cancha_id, usuario_rut) VALUES
(CURDATE(), '18:00:00', 25000.00, 2, 1, '22.222.222-2'),
(CURDATE(), '19:00:00', 25000.00, 1, 1, '33.333.333-3');

-- Partidos y Walkover
-- Escenario normal
INSERT INTO partidos (torneo_id, equipo_1_id, equipo_2_id, reserva_cancha_id, resultado_equipo_1, resultado_equipo_2) VALUES
(1, 1, 2, 1, 2, 1);

-- Escenario Walkover (Probando la regla 3-0)
INSERT INTO partidos (torneo_id, equipo_1_id, equipo_2_id, reserva_cancha_id, resultado_equipo_1, resultado_equipo_2, es_walkover, equipo_perdedor_id) VALUES
(1, 2, 1, 2, 3, 0, TRUE, 1);
