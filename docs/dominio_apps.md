# Arquitectura de Dominio (Domain-Driven Design)

En este proyecto utilizamos un enfoque de diseño modular basado en el concepto de **Dominio**. El objetivo principal es mantener el código altamente cohesionado, evitando las aplicaciones "obesas" (God Apps) y asegurando que cada módulo sea independiente y mantenible.

## 🏛️ Principio de Responsabilidad Única (SRP)

Cada aplicación (`app`) de Django en este proyecto es dueña absoluta de su "Dominio de Conocimiento". Esto significa que:
1.  **Backend y UI van juntos:** Si una app procesa la lógica de Reservas, esa misma app debe alojar los *templates* y la experiencia de usuario (UX) correspondiente a las Reservas.
2.  **Bajo Acoplamiento:** Las apps se comunican entre sí mediante referencias simples (ej. Claves Foráneas o IDs) en lugar de compartir lógica compleja.
3.  **Independencia (Pluggable):** Si en el futuro un módulo (ej. Penalizaciones) ya no es requerido, se debería poder eliminar la carpeta de la app con un impacto mínimo o nulo en el resto del sistema.

## 📦 Definición de Dominios por App

A continuación, se detalla la responsabilidad exclusiva de cada aplicación:

### 1. 🟢 App `users` (Dominio de Identidad)
*   **Responsabilidad:** ¿Quién eres y qué permiso tienes?
*   **Límites:** Gestiona el registro, la autenticación (Login/Logout), el hashing de contraseñas, los roles (Admin, Cliente, etc.) y los estados básicos (Activo, Bloqueado).
*   **Lo que NO hace:** No calcula descuentos, no sabe cuántas faltas tiene un usuario, ni sabe qué canchas ha arrendado.

### 2. 🟡 App `memberships` (Dominio de Privilegios)
*   **Responsabilidad:** ¿Qué beneficios tienes según tu nivel?
*   **Límites:** Gestiona los tipos de planes (VIP, Socio, Normal), los porcentajes de descuento y los costos mensuales. Es dueña de la interfaz "Mis Beneficios" donde el cliente ve su estado.
*   **Lo que NO hace:** No gestiona el perfil base del usuario. Solo se asocia a un RUT para otorgar la regla de negocio del descuento.

### 3. 🔵 App `courts` (Dominio de Infraestructura)
*   **Responsabilidad:** ¿Dónde se juega y cuánto cuesta la hora base?
*   **Límites:** Mantiene el catálogo físico del recinto (Canchas, Quinchos, Superficies). Define el valor bruto por hora antes de cualquier descuento.
*   **Lo que NO hace:** No sabe si la cancha está ocupada en un horario específico (eso es una transacción, no infraestructura).

### 4. 🔴 App `bookings` (Dominio Transaccional) - *Corazón del Sistema*
*   **Responsabilidad:** ¿Quién reservó qué, cuándo y cuánto pagó finalmente?
*   **Límites:** Coordina la relación entre un Usuario (`users`), una Infraestructura (`courts`) y un Horario.
*   **Interacción con otros dominios:** Al momento de cobrar, `bookings` le "pregunta" a `memberships` qué descuento aplicar sobre el precio base que dictó `courts`.

### 5. 🟠 App `penalties` (Dominio de Consecuencias)
*   **Responsabilidad:** ¿Quién no cumplió las reglas y qué castigo recibe?
*   **Límites:** Registra los "No-shows" (inasistencias) leyendo el historial de `bookings`, calcula multas progresivas y es capaz de emitir una orden para cambiar el estado de un usuario en la app `users` (ej. a "Bloqueado").

## 💡 Resumen Práctico

> *"A `users` no le importa cuánto cuesta ser VIP, solo sabe que tienes la etiqueta VIP.*
> *A `memberships` no le importa cuándo reservaste una cancha, solo sabe que por ser VIP te debe descontar un 15%.*
> *A `bookings` no le importa cómo te llamas ni tu contraseña, solo junta tu ID con una cancha y calcula tu total."*