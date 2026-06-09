# Arquitectura del Sistema (Django Apps)

El sistema se divide en 7 aplicaciones modulares, centralizadas mediante un núcleo de infraestructura, para garantizar escalabilidad, seguridad y coherencia visual.

## 📂 Estructura de Aplicaciones

### 1. `core` (Infraestructura y Orquestación)
- **Propósito:** El "corazón" técnico del proyecto. Centraliza los activos estáticos (Bootstrap, jQuery, alert.js), las plantillas base (`base.html`, `auth_base.html`) y los Dashboards de usuario.
- **Responsabilidad:** Garantizar la consistencia visual y el control de sesiones (inactividad).

### 2. `users` (Gestión de Identidad)
- **Propósito:** Manejo de perfiles de usuario, roles y seguridad administrativa.
- **Requerimientos:** RF-01, RF-02, RF-03, RF-04.

### 3. `authentication` (Acceso y Seguridad)
- **Propósito:** Control de flujo de Login, Registro, Logout y decoradores de seguridad.

### 4. `memberships` (Niveles y Beneficios)
- **Propósito:** Gestión de planes (VIP/Socio) y lógica de descuentos aplicada al cliente.
- **Requerimientos:** RF-05, RF-06.

### 5. `courts` (Infraestructura Deportiva)
- **Propósito:** Gestión unificada de Canchas y Quinchos. Define características físicas y valores base.
- **Requerimientos:** RF-07, RF-08.

### 6. `bookings` (Motor Transaccional)
- **Propósito:** Gestión del calendario de disponibilidad, reservas en tiempo real y flujo de pagos.
- **Requerimientos:** RF-09, RF-10, RF-20.

### 7. `penalties` (Disciplina y Control)
- **Propósito:** Registro de faltas, multas progresivas (50%/100%) e inasistencias automáticas.
- **Requerimientos:** RF-11, RF-12, RF-13.

---

## 🚀 Visión del Producto (Estructura de Acceso)

El sistema implementa un modelo de **Control de Acceso Basado en Roles (RBAC)**:

### 1. Catálogo de Cliente (B2C)
- **Audiencia:** Clientes finales.
- **Experiencia:** Vista de "Catálogo" en Infraestructura y Membresías (sin botones administrativos). Acceso directo a reservas y gestión de deudas propias.

### 2. Panel Administrativo (ERP)
- **Audiencia:** Staff del recinto (Admin, Recepcionistas).
- **Experiencia:** Gestión total de usuarios, infraestructura, penalizaciones manuales y registro de inasistencias (No-show).

---

## 🛠️ Estándares Técnicos (Actualizados)
- **Capa de Datos:** Uso estricto de **SQL Manual** vía `DatabaseManager` (PyMySQL). El ORM de Django se evita para mantener control total sobre las queries.
- **Activos Centralizados:** Carga única de librerías en la app `core` para mejorar el rendimiento y mantenimiento.
- **Seguridad de Sesión:** Implementación de **Logout Automático** tras 15 minutos de inactividad, con alerta visual preventiva al minuto 13.
- **Internacionalización (i18n):** URLs estandarizadas en inglés y formatos de moneda en pesos chilenos (CLP) con separadores de miles.
