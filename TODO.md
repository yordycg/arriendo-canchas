# Roadmap de Desarrollo - Arriendo Canchas

Este archivo marca el progreso de implementación del sistema.

## 🟢 Fase 1: Identidad y Acceso (Prioridad Alta)
- [ ] Configurar Proyecto Django Base (Settings, Base de Datos PyMySQL).
- [ ] Implementar App `users`: Modelo de usuario personalizado (RUT), Login y Roles.
- [ ] Implementar App `memberships`: Gestión de niveles VIP/Socio y lógica de descuentos.

## 🔵 Fase 2: Infraestructura y Catálogo (Prioridad Media)
- [ ] Implementar App `courts`: CRUD de canchas, tipos y superficies.
- [ ] Implementar App `pavilions`: CRUD de quinchos y restricción VIP.

## 🟠 Fase 3: Operación Central (Prioridad Crítica)
- [ ] Implementar App `bookings`: Motor de reservas de canchas y quinchos.
- [ ] Implementar validación de disponibilidad y prevención de sobrecupo.
- [ ] Implementar lógica de cancelación (Regla 30 min / 15 min).

## 🔴 Fase 4: Disciplina y Control
- [ ] Implementar App `penalties`: Registro de faltas y contador progresivo.
- [ ] Implementar bloqueo automático de reservas por reincidencia.

## 🏆 Fase 5: Competición
- [ ] Implementar App `tournaments`: Gestión de torneos y equipos.
- [ ] Implementar registro de partidos y Regla de Walkover (3-0).

---

## 🛠️ Tareas Técnicas Globales
- [ ] Integrar Bootstrap 5 y jQuery en los templates base.
- [ ] Configurar variables de entorno (.env) en Django.
- [ ] Crear Suite de Tests inicial para cada aplicación.
