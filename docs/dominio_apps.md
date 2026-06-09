# Arquitectura de Dominio (Domain-Driven Design)

En este proyecto utilizamos un enfoque de diseño modular basado en el concepto de **Dominio**. El objetivo principal es mantener el código altamente cohesionado, evitando las aplicaciones "obesas" (God Apps) y asegurando que cada módulo sea independiente y mantenible.

## 🏛️ Principio de Responsabilidad Única (SRP)

Cada aplicación (`app`) de Django en este proyecto es dueña absoluta de su "Dominio de Conocimiento". Esto significa que:
1.  **Backend y UI van juntos:** Si una app procesa la lógica de Reservas, esa misma app debe alojar los *templates* y la experiencia de usuario (UX) correspondiente a las Reservas.
2.  **Bajo Acoplamiento:** Las apps se comunican entre sí mediante referencias simples (ej. Claves Foráneas o IDs) en lugar de compartir lógica compleja.
3.  **Independencia (Pluggable):** Si en el futuro un módulo (ej. Penalizaciones) ya no es requerido, se debería poder eliminar la carpeta de la app con un impacto mínimo o nulo en el resto del sistema.

## 📦 Definición de Dominios por App

A continuación, se detalla la responsabilidad exclusiva de cada aplicación:

### 1. 🔘 App `core` (Dominio de Soporte y Orquestación)
*   **Responsabilidad:** ¿Cómo se ve el sistema y cómo se mantienen las sesiones?
*   **Límites:** Centraliza el diseño base (`base.html`), las librerías CSS/JS compartidas y los Dashboards. Controla la seguridad por inactividad y garantiza que el sistema sea consistente visualmente.

### 2. 🟢 App `users` (Dominio de Identidad)
*   **Responsabilidad:** ¿Quién eres y qué permiso tienes?
*   **Límites:** Gestiona el perfil del usuario (RUT, Nombre, Email), su estado administrativo y su rol.
*   **Lo que NO hace:** No gestiona el flujo de Login (eso es de `authentication`) ni calcula descuentos de membresía.

### 3. 🟡 App `memberships` (Dominio de Privilegios)
*   **Responsabilidad:** ¿Qué beneficios tienes según tu nivel?
*   **Límites:** Gestiona los tipos de planes y los descuentos globales. Es dueña de la interfaz "Mis Beneficios" donde el cliente ve su estado de socio.

### 4. 🔵 App `courts` (Dominio de Infraestructura)
*   **Responsabilidad:** ¿Dónde se juega y cuánto cuesta la hora base?
*   **Límites:** Mantiene el catálogo físico del recinto (**Canchas y Quinchos**). Define el valor bruto antes de cualquier descuento.

### 5. 🔴 App `bookings` (Dominio Transaccional) - *Corazón del Sistema*
*   **Responsabilidad:** ¿Quién reservó qué, cuándo y cuánto pagó finalmente?
*   **Límites:** Coordina la relación entre un Usuario, una Infraestructura y un Horario.
*   **Interacción:** Al momento de cobrar, `bookings` consulta a `memberships` para aplicar el descuento correspondiente.

### 6. 🟠 App `penalties` (Dominio de Consecuencias)
*   **Responsabilidad:** ¿Quién no cumplió las reglas y qué castigo recibe?
*   **Límites:** Registra inasistencias (**No-shows**) y calcula multas progresivas. Es capaz de bloquear a un usuario si acumula demasiadas deudas.

## 💡 Resumen Práctico

> *"A `users` no le importa cuánto cuesta ser VIP, solo sabe que tienes la etiqueta VIP.*
> *A `core` no le importa qué reservaste, solo le importa que sigas activo para no cerrar tu sesión.*
> *A `bookings` no le importa cómo te llamas, solo junta tu ID con una cancha y calcula tu total."*
