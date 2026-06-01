# Valores Predeterminados (DEFAULTS) del Sistema

Este documento describe los valores predeterminados aplicados directamente en el esquema de la base de datos (`01_schema.sql`) para asegurar la consistencia de los datos y simplificar las operaciones de inserción.

## 1. Gestión de Usuarios
Al registrar un nuevo usuario (vía registro propio o administrativo), se aplican los siguientes valores por defecto:

| Columna | Valor Default | Descripción |
| :--- | :--- | :--- |
| `estado_usuario_id` | `1` (Activo) | El usuario queda habilitado inmediatamente. |
| `rol_id` | `3` (Cliente) | Perfil estándar de acceso al sistema. |
| `membresia_id` | `1` (Normal) | Nivel base sin beneficios adicionales. |
| `sexo` | `'O'` (Otro) | Clasificación neutra inicial. |

## 2. Quinchos y Canchas
Asegura que las nuevas instalaciones tengan valores numéricos base y estados operativos iniciales.

| Tabla | Columna | Valor Default | Descripción |
| :--- | :--- | :--- | :--- |
| `quinchos` | `solo_vip` | `FALSE` | Acceso general por defecto. |
| `quinchos` | `estado_quincho_id` | `1` (Disponible) | Listo para reserva inmediata. |
| `quinchos` | `valor_reserva` | `0.00` | Costo base inicial. |
| `canchas` | `valor_hora` | `0.00` | Costo base inicial por hora. |

## 3. Reservas (Canchas y Quinchos)
Estandariza el estado inicial de toda transacción de reserva.

| Columna | Valor Default | Descripción |
| :--- | :--- | :--- |
| `estado_id` | `1` (Pendiente) | Toda reserva nace esperando confirmación o pago. |
| `valor_pagado` | `0.00` | Saldo inicial al momento de la creación. |

## 4. Penalizaciones y Membresías
Valores de configuración y registro transaccional.

| Tabla | Columna | Valor Default | Descripción |
| :--- | :--- | :--- | :--- |
| `usuarios_penalizaciones` | `fecha` | `CURRENT_DATE` | Fecha automática del registro de la falta. |
| `membresias` | `porcentaje_descuento` | `0` | Sin descuento inicial. |
| `membresias` | `costo_mensual` | `0.00` | Sin costo recurrente inicial. |
| `tipos_penalizaciones` | `valor_multa` | `0.00` | Monto base para multas. |
| `tipos_penalizaciones` | `dias_bloqueo` | `0` | Sin suspensión temporal inicial. |

## 5. Auditoría de Login
Valores automáticos para el registro de seguridad.

| Tabla | Columna | Valor Default | Descripción |
| :--- | :--- | :--- | :--- |
| `auditoria_login` | `fecha_hora` | `CURRENT_TIMESTAMP` | Registro exacto del momento del intento. |
| `auditoria_login` | `created_at` | `CURRENT_TIMESTAMP` | Marca de tiempo de creación del registro. |
