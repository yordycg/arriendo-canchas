# Documentación de la Base de Datos - Sistema de Arriendo

Este documento centraliza toda la información referente al diseño, reglas y estructura de la base de datos del sistema.

## 📊 Diagrama Relacional

![Diagrama de Base de Datos](./diagrama.png)

> **Nota:** Para editar este diagrama, utiliza el archivo fuente [diagram.dbml](./diagram.dbml) en [dbdiagram.io](https://dbdiagram.io).

---

## 📜 Reglas de Negocio

### Canchas
- Una cancha no puede ser reservada por más de un usuario en el mismo bloque horario.

### Reservas
- Las cancelaciones deben realizarse con un mínimo de **30 minutos** de anticipación.
- Cancelaciones fuera de plazo generan una **penalización** automática al usuario.

### Usuarios
- El sistema bloqueará la cuenta tras **3 intentos fallidos** de inicio de sesión.

---

## 🔄 Relaciones Principales

| Tabla A (1) | Tabla B (N) | Descripción |
| :--- | :--- | :--- |
| **tipo_canchas** | **canchas** | Un deporte puede tener múltiples canchas. |
| **usuarios** | **reservas_canchas** | Un usuario gestiona sus propios arriendos. |
| **torneos** | **partidos** | Un torneo agrupa múltiples encuentros deportivos. |
| **equipos** | **equipo_usuarios** | Relación N:M para conformar los planteles. |

---

## 🗂️ Entidades y Atributos

### Núcleo de Arriendo
- **canchas:** `nombre`, `valor_hora`, `tipo_superficie`, `tipo_recinto`.
- **reservas_canchas:** `fecha`, `hora`, `valor_pagado` (histórico), `estado_id`.
- **quinchos:** `nombre`, `valor_reserva`, `solo_vip` (Boolean).

### Usuarios y Roles
- **usuarios:** `rut` (PK), `nombres`, `email`, `password`, `membresia_id`.
- **membresias:** `nombre` (Normal, VIP, Socio), `porcentaje_descuento`.
- **penalizaciones:** `valor_multa`, `dias_bloqueo`.

### Torneos y Equipos
- **torneos:** `nombre`, `fecha_inicio`, `fecha_fin`.
- **partidos:** `equipo_1`, `equipo_2`, `resultado_1`, `resultado_2`.
- **equipos:** `nombre`, `capitan_id`.

---

## 🛠️ Instrucciones de Mantenimiento

1. **Modificación del esquema:** Editar `diagram.dbml` y actualizar la imagen `arriendo_canchas_db.svg`.
2. **Nuevas Reglas:** Actualizar la sección correspondientes en este README.
3. **Integridad:** Se recomienda el uso de `PROTECT` en llaves foráneas para evitar borrados accidentales de configuración.
