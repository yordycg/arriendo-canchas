# Arquitectura del Sistema (Django Apps)

El sistema se divide en 7 aplicaciones modulares para garantizar escalabilidad y desacoplamiento.

## 📂 Estructura de Aplicaciones

### 1. `users`
- **Modelos:** `User` (Custom), `Role`, `UserStatus`.
- **Propósito:** Manejo de identidad, autenticación y niveles de acceso.
- **Requerimientos:** RF-01, RF-02, RF-03, RF-04.

### 2. `memberships`
- **Modelos:** `Membership`.
- **Propósito:** Gestión de planes (VIP/Socio) y lógica de descuentos globales.
- **Requerimientos:** RF-05, RF-06.

### 3. `courts`
- **Modelos:** `Court`, `CourtType`.
- **Propósito:** Gestión de la infraestructura de canchas y sus características físicas.
- **Requerimientos:** RF-07.

### 4. `pavilions`
- **Modelos:** `Pavilion`, `PavilionStatus`.
- **Propósito:** Gestión de quinchos y validación de acceso exclusivo VIP.
- **Requerimientos:** RF-08.

### 5. `bookings`
- **Modelos:** `CourtReservation`, `PavilionReservation`.
- **Propósito:** El motor transaccional del sistema. Gestiona el calendario y pagos.
- **Requerimientos:** RF-09, RF-10.

### 6. `penalties`
- **Modelos:** `Penalty`, `PenaltyType`.
- **Propósito:** Control de disciplina, recargos progresivos y bloqueos de cuenta.
- **Requerimientos:** RF-11, RF-12, RF-13.

### 7. `tournaments`
- **Modelos:** `Tournament`, `Team`, `Match`.
- **Propósito:** Organización de ligas y competencia deportiva.
- **Requerimientos:** RF-14, RF-15.

---

## 🚀 Visión del Producto (Estructura de Acceso)

Para cumplir con los objetivos comerciales y de usuario, el sistema se divide en dos grandes áreas:

### 1. Portal Público (Landing Page)
- **Audiencia:** Usuarios no registrados, visitantes y clientes potenciales.
- **Contenido:** Catálogo de canchas, servicios (quinchos), precios y testimonios.
- **Acciones:** Registro de nuevos socios (Auto-registro) e Inicio de Sesión.

### 2. Panel Administrativo (SaaS Web App)
- **Audiencia:** Staff del recinto (Admin, Vendedores, Recepcionistas).
- **Contenido:** Gestión de usuarios, configuración de canchas, reportes y penalizaciones.
- **Acciones:** CRUD total del sistema y gestión de membresías especiales.

---

## 🛠️ Estándares Técnicos (Actualizados)
- **Capa de Datos:** Uso estricto de **SQL Manual** vía `DatabaseManager`. Se omite el ORM de Django para lógica de negocio.
- **Vistas:** Se utilizarán *Function-Based Views (FBV)* para mayor control del flujo manual.
- **Seguridad:** Control de acceso mediante **Decoradores Manuales** (`@login_required_manual`, `@role_required`) que validan la sesión en la base de datos.
- **Sesiones:** Manejo persistente en el servidor para rastrear RUT, Rol y Membresía del usuario.
