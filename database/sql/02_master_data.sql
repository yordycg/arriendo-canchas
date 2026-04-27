-- DATOS MAESTROS (Obligatorios para el funcionamiento del sistema)
USE arriendo_canchas_db;

-- Estados de Usuarios
INSERT INTO estados_usuarios (nombre) VALUES 
('Activo'), ('Inactivo'), ('Bloqueado por Deuda'), ('Bloqueado por Seguridad');

-- Estados de Reservas
INSERT INTO estados_reservas (nombre) VALUES 
('Pendiente'), ('Pagada'), ('Cancelada'), ('No Asistida (W.O.)');

-- Estados de Quinchos
INSERT INTO estados_quinchos (nombre) VALUES 
('Disponible'), ('Ocupado'), ('Mantenimiento');

-- Roles de Sistema
INSERT INTO roles (nombre) VALUES 
('Admin'), ('Recepcionista'), ('Cliente'), ('Invitado');

-- Membresías (Según políticas.md)
INSERT INTO membresias (nombre, porcentaje_descuento, costo_mensual) VALUES 
('Normal', 0, 0.00),
('VIP', 15, 15000.00),
('Socio', 30, 25000.00);

-- Tipos de Canchas
INSERT INTO tipos_canchas (nombre) VALUES 
('Futbol 5'), ('Futbol 7'), ('Futbol 11'), ('Tenis'), ('Padel'), ('Basquetbol');

-- Tipos de Penalizaciones
INSERT INTO tipos_penalizaciones (nombre, descripcion, valor_multa, dias_bloqueo) VALUES 
('No show', 'El usuario no se presentó a la reserva', 5000.00, 2),
('Cancelación tardía', 'Cancelación con menos de 30 min de aviso', 3000.00, 0),
('Mal comportamiento', 'Daños o disturbios en el recinto', 20000.00, 30),
('Walkover Torneo', 'Inasistencia a partido de torneo (Capitán responsable)', 10000.00, 7);
