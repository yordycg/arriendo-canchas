# Roadmap de Desarrollo - Arriendo Canchas

Este archivo marca el progreso de implementación del sistema siguiendo la **Ruta Ideal de Construcción** para asegurar testeabilidad inmediata.

## 🟢 Fase 1: Identidad y Acceso (COMPLETADO)

- [x] Configurar Proyecto Django Base (Settings, Base de Datos PyMySQL).
- [x] Implementar App `users`: Modelo de usuario personalizado (RUT), Login y Roles.
  - [x] **Login/Logout Base:** Autenticación manual con SQL y manejo de sesiones.
  - [x] **Auditoría de Login:** Registro automático en `auditoria_login` (Correcto/Incorrecto + Password fallida).
  - [x] **Control de Acceso (Decoradores):** Implementar `@login_required_manual` y `@role_required` para proteger rutas.
  - [x] **Secure Auth:** Implementar hashing de contraseñas PBKDF2 y protección contra fuerza bruta.
  - [x] **Public Registration:** Implementar formulario de auto-registro para Clientes.
  - [x] **SweetAlert2 Standard:** Integrado en flujos de Autenticación y Usuarios.
  - [ ] **Buscador Dinámico:** Filtro de usuarios por RUT, Nombre o Email en el listado.
  - [ ] **Paginación Senior:** Mostrar solo 10 registros por página con controles de navegación (Next/Prev).
  - [ ] **Panel de Recuperación:** Interfaz para administrar usuarios inactivos y permitir su reactivación.

## 🏗️ Ruta Ideal de Construcción (Pendiente)

Sigue este orden para garantizar que cada módulo tenga sus dependencias listas para probar:

### 1. 🟢 App `courts`: Infraestructura Base (COMPLETADO)
- [x] CRUD de Canchas (Listado, Creación, Edición, Eliminación).
- [x] CRUD de Quinchos (con flag de `solo_vip`).
- [x] Gestión de tipos de canchas y superficies.
- [ ] **Consumo de API (Clima):** Pendiente para la fase final.

### 2. 🟡 App `memberships`: Reglas de Negocio y Precios
- [ ] CRUD de Planes (Normal, VIP, Socio) con sus porcentajes de descuento.
- [ ] Lógica de asociación de membresía al perfil de usuario.
- [ ] Vista de beneficios según nivel de socio.

### 3. 🔴 App `bookings`: Motor Transaccional (EL CORAZÓN)
- [ ] Motor de reservas de canchas y quinchos (SQL Manual).
- [ ] **Prevención de Sobrecupo:** Validación de disponibilidad única por recurso/fecha/hora.
- [ ] **Cálculo Dinámico:** Aplicar descuentos según membresía del usuario en tiempo real.
- [ ] Lógica de cancelación (Regla 30 min / 15 min según nivel).

### 4. 🟠 App `penalties`: Disciplina y Control
- [ ] Registro automático de inasistencias (No-shows).
- [ ] Cálculo de multas progresivas (Escala 50% - 100%).
- [ ] **Bloqueo de Cuenta:** Impedir nuevas reservas si el usuario tiene >= 5 faltas.

## 🏆 Fase Final: Competición y Cierre
- [ ] Implementar App `tournaments`: Gestión de torneos y equipos.
- [ ] Implementar registro de partidos y Regla de Walkover (3-0).
- [ ] Generación de Manual de Desarrollo (Documentación Final).
