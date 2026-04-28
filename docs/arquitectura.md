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

## 🛠️ Estándares de Comunicación
- **Vistas:** Se utilizarán *Class-Based Views (CBV)* para consistencia.
- **Validaciones:** Las reglas de negocio se validarán en el método `clean()` de los modelos o en los *Forms*.
- **Seguridad:** Uso de Mixins para control de acceso basado en el rol del usuario.
