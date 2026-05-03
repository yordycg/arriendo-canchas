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

---

## 🚀 Evolución Profesional & Estándares Senior (Próximos Proyectos)

- [ ] **Docker-Compose Total:** Implementar Docker para el ciclo de vida completo (DB + App + Cache) en lugar de ejecuciones híbridas.
- [ ] **direnv & Automatización:** Configurar activación automática de entornos virtuales (`layout python`) y carga de secretos al entrar al directorio.
- [ ] **Agnosticismo de Shell:** Perfeccionar el uso de `justfile` para ocultar la complejidad del OS.

## ✅ Tareas Técnicas Completadas

- [x] Implementar DEFAULTS en esquema SQL (`01_schema.sql`).
- [x] Sincronizar documentación técnica (`entidades_atributos.md`, `diagram.dbml`, `relaciones.md`).
- [x] Crear `justfile` multiplataforma para automatización de tareas.
- [x] Definir Estándares de Valores Predeterminados en `defaults.md`.
