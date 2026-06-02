SET NAMES 'utf8mb4';
CREATE DATABASE IF NOT EXISTS arriendo_canchas_db;

USE arriendo_canchas_db;

--
CREATE TABLE estados_usuarios (
  estado_usuario_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE estados_reservas (
  estado_reserva_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE estados_quinchos (
  estado_quincho_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE roles (
  rol_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE membresias (
  membresia_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  porcentaje_descuento INT NOT NULL DEFAULT 0 CHECK (porcentaje_descuento BETWEEN 0 AND 100),
  costo_mensual DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (costo_mensual >= 0),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE tipos_canchas (
  tipo_cancha_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE tipos_penalizaciones (
  tipo_penalizacion_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion TEXT,
  valor_multa DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (valor_multa >= 0),
  dias_bloqueo INT DEFAULT 0 CHECK (dias_bloqueo >= 0),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

--
CREATE TABLE canchas (
  cancha_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  valor_hora DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (valor_hora >= 0),
  tipo_superficie VARCHAR(50) NOT NULL CHECK (tipo_superficie IN ('Pasto Sintetico', 'Pasto Natural', 'Arcilla', 'Cemento', 'Parquet', 'Baldosa')),
  tipo_recinto VARCHAR(50) NOT NULL CHECK (tipo_recinto IN ('Abierto', 'Semi-techado', 'Cerrado')),
  tipo_cancha_id INT NOT NULL, -- FK tipos_canchas.tipo_cancha_id
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_cancha_tipo FOREIGN KEY (tipo_cancha_id) REFERENCES tipos_canchas (tipo_cancha_id) ON DELETE RESTRICT
);

CREATE TABLE torneos (
  torneo_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  tipo_cancha_id INT NOT NULL, -- FK tipos_canchas.tipo_cancha_id
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_torneo_tipo_cancha FOREIGN KEY (tipo_cancha_id) REFERENCES tipos_canchas (tipo_cancha_id) ON DELETE RESTRICT,
  CONSTRAINT ck_torneo_fechas CHECK (fecha_fin >= fecha_inicio)
);

CREATE TABLE usuarios (
  rut VARCHAR(12) PRIMARY KEY,
  nombres VARCHAR(100) NOT NULL,
  apellido_p VARCHAR(100),
  apellido_m VARCHAR(100),
  sexo CHAR(1) DEFAULT 'O' CHECK (sexo IN ('M', 'F', 'O')),
  telefono VARCHAR(15),
  email VARCHAR(150) UNIQUE,
  password VARCHAR(255),
  intentos_fallidos INT DEFAULT 0,
  contador_faltas INT DEFAULT 0,
  estado_usuario_id INT NOT NULL DEFAULT 1, -- FK estados_usuarios.estado_usuario_id
  rol_id INT NOT NULL DEFAULT 3, -- FK roles.rol_id
  membresia_id INT, -- FK membresias.membresia_id
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_usuario_estado FOREIGN KEY (estado_usuario_id) REFERENCES estados_usuarios (estado_usuario_id) ON DELETE RESTRICT,
  CONSTRAINT fk_usuario_rol FOREIGN KEY (rol_id) REFERENCES roles (rol_id) ON DELETE RESTRICT,
  CONSTRAINT fk_usuario_membresia FOREIGN KEY (membresia_id) REFERENCES membresias (membresia_id) ON DELETE RESTRICT
);

CREATE TABLE quinchos (
  quincho_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  valor_reserva DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (valor_reserva >= 0),
  solo_vip BOOLEAN NOT NULL DEFAULT FALSE,
  estado_quincho_id INT NOT NULL DEFAULT 1, -- FK estados_quinchos.estado_quincho_id
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_quincho_estado FOREIGN KEY (estado_quincho_id) REFERENCES estados_quinchos (estado_quincho_id) ON DELETE RESTRICT
);

CREATE TABLE reservas_canchas (
  reserva_cancha_id INT PRIMARY KEY AUTO_INCREMENT,
  fecha DATE NOT NULL,
  hora TIME NOT NULL,
  valor_pagado DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (valor_pagado >= 0),
  estado_id INT NOT NULL DEFAULT 1, -- FK estados_reservas.estado_reserva_id
  cancha_id INT NOT NULL, -- FK canchas.cancha_id
  usuario_rut VARCHAR(12) NOT NULL, -- FK usuarios.rut
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT uq_reserva_cancha UNIQUE (cancha_id, fecha, hora),
  CONSTRAINT fk_reserva_cancha_estado FOREIGN KEY (estado_id) REFERENCES estados_reservas (estado_reserva_id) ON DELETE RESTRICT,
  CONSTRAINT fk_reserva_cancha_cancha FOREIGN KEY (cancha_id) REFERENCES canchas (cancha_id) ON DELETE RESTRICT,
  CONSTRAINT fk_reserva_cancha_usuario FOREIGN KEY (usuario_rut) REFERENCES usuarios (rut) ON DELETE RESTRICT
);

CREATE TABLE reservas_quinchos (
  reserva_quincho_id INT PRIMARY KEY AUTO_INCREMENT,
  fecha DATE NOT NULL,
  hora TIME NOT NULL,
  valor_pagado DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (valor_pagado >= 0),
  estado_id INT NOT NULL DEFAULT 1, -- FK estados_reservas.estado_reserva_id
  quincho_id INT NOT NULL, -- FK quinchos.quincho_id
  usuario_rut VARCHAR(12) NOT NULL, -- FK usuarios.rut
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT uq_reserva_quincho UNIQUE (quincho_id, fecha, hora),
  CONSTRAINT fk_reserva_quincho_estado FOREIGN KEY (estado_id) REFERENCES estados_reservas (estado_reserva_id) ON DELETE RESTRICT,
  CONSTRAINT fk_reserva_quincho_quincho FOREIGN KEY (quincho_id) REFERENCES quinchos (quincho_id) ON DELETE RESTRICT,
  CONSTRAINT fk_reserva_quincho_usuario FOREIGN KEY (usuario_rut) REFERENCES usuarios (rut) ON DELETE RESTRICT
);

CREATE TABLE equipos (
  equipo_id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  capitan_id VARCHAR(12) NOT NULL, -- FK usuarios.rut
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_equipo_usuario FOREIGN KEY (capitan_id) REFERENCES usuarios (rut) ON DELETE RESTRICT
);

CREATE TABLE equipos_usuarios (
  equipo_id INT NOT NULL, -- FK equipos.equipo_id
  usuario_rut VARCHAR(12) NOT NULL, -- FK usuarios.rut
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (equipo_id, usuario_rut),
  CONSTRAINT fk_equipo_usuario_equipo FOREIGN KEY (equipo_id) REFERENCES equipos (equipo_id) ON DELETE RESTRICT,
  CONSTRAINT fK_equipo_usuario_usuario FOREIGN KEY (usuario_rut) REFERENCES usuarios (rut) ON DELETE RESTRICT
);

CREATE TABLE partidos (
  partido_id INT PRIMARY KEY AUTO_INCREMENT,
  torneo_id INT NOT NULL, -- FK torneos.torneo_id
  equipo_1_id INT NOT NULL, -- FK equipos.equipo_id
  equipo_2_id INT NOT NULL, -- FK equipos.equipo_id
  reserva_cancha_id INT NOT NULL, -- FK reservas_canchas.reserva_cancha_id
  resultado_equipo_1 INT NOT NULL DEFAULT 0 CHECK (resultado_equipo_1 >= 0),
  resultado_equipo_2 INT NOT NULL DEFAULT 0 CHECK (resultado_equipo_2 >= 0),
  es_walkover BOOLEAN DEFAULT FALSE,
  equipo_perdedor_id INT, -- FK equipos.equipo_id (quien no asistió)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_partido_torneo FOREIGN KEY (torneo_id) REFERENCES torneos (torneo_id) ON DELETE RESTRICT,
  CONSTRAINT fk_partido_equipo_1 FOREIGN KEY (equipo_1_id) REFERENCES equipos (equipo_id) ON DELETE RESTRICT,
  CONSTRAINT fk_partido_equipo_2 FOREIGN KEY (equipo_2_id) REFERENCES equipos (equipo_id) ON DELETE RESTRICT,
  CONSTRAINT fk_partido_reserva_cancha FOREIGN KEY (reserva_cancha_id) REFERENCES reservas_canchas (reserva_cancha_id) ON DELETE RESTRICT,
  CONSTRAINT fk_partido_equipo_perdedor FOREIGN KEY (equipo_perdedor_id) REFERENCES equipos (equipo_id) ON DELETE RESTRICT,
  CONSTRAINT ck_partido_equipos CHECK (equipo_1_id <> equipo_2_id),
  CONSTRAINT ck_walkover_equipo CHECK (equipo_perdedor_id IS NULL OR equipo_perdedor_id IN (equipo_1_id, equipo_2_id)),
  CONSTRAINT ck_walkover_resultado CHECK (
    es_walkover = FALSE OR
    (resultado_equipo_1 = 3 AND resultado_equipo_2 = 0) OR
    (resultado_equipo_1 = 0 AND resultado_equipo_2 = 3)
  )
);

CREATE TABLE usuarios_penalizaciones (
  usuario_penalizado_id INT PRIMARY KEY AUTO_INCREMENT,
  usuario_rut VARCHAR(12) NOT NULL, -- FK usuarios.rut
  tipo_penalizacion_id INT NOT NULL, -- FK tipos_penalizaciones.tipo_penalizacion_id
  fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
  pagada BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_usuario_penalizacion_usuario FOREIGN KEY (usuario_rut) REFERENCES usuarios (rut) ON DELETE RESTRICT,
  CONSTRAINT fk_usuario_penalizacion_tipo FOREIGN KEY (tipo_penalizacion_id) REFERENCES tipos_penalizaciones (tipo_penalizacion_id) ON DELETE RESTRICT
);

CREATE TABLE auditoria_login (
  auditoria_id INT PRIMARY KEY AUTO_INCREMENT,
  usuario VARCHAR(150) NOT NULL, -- RUT o Email
  fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  estado_login VARCHAR(20) NOT NULL CHECK(estado_login IN ('Correcto', 'Incorrecto')),
  password_ingresada VARCHAR(255), -- Solo registrar si el 'estado_login' = 'Incorrecto'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
