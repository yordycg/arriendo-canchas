# TASKS — arriendo-canchas

> Fuente de verdad del trabajo **de los proyectos**. Una fase activa a la vez.
> El portfolio (`yordycg-portfolio`) queda bloqueado hasta `v2.0`; no se duplica aquí su roadmap.
> Última actualización: 2026-11-01

## Estado actual

- **Release vigente:** `v1.0-academica` — estado congelado, sin tests.
- **Fase activa:** F0 — Higiene y línea base.
- **Próxima acción:** F0.4.
- **Objetivo de `v2.0`:** núcleo reescrito y defendible, tests verdes en CI, demo desplegada, caso de estudio publicado.

## Convenciones

- `[ ]` pendiente · `[x]` completado · `[~]` en curso.
- ID de tarea: `F0.1`, `F1.2`, …
- Zona según `AGENTS.md` §4: **[R]** roja (la escribe Yordy), **[V]** verde (la puede escribir la IA), **[A]** azul (IA obligatoria: revisión, casos borde, defensa).
- Estimación en horas de trabajo efectivo.
- No se abre una fase nueva hasta cerrar la anterior.

---

## F0 — Higiene y línea base

**Estado:** en curso · **Estimación:** 6–8 h

**Objetivo:** que el repositorio diga la verdad antes de tocarlo. `main` al día, `AGENTS.md` como única fuente, README sin filtraciones y dependencias separadas.

**Criterio de salida:** `main` refleja el estado real con tag, no hay referencias rotas, el README no expone credenciales, y `just check` existe (aunque la suite esté vacía).

- [x] **F0.1** [V] Tag `v1.0-academica` en `develop` y fast-forward de `main` (`git push origin develop:main`). Desde aquí, `main` solo recibe `v2.0`.
- [x] **F0.2** [V] `AGENTS.md` creado; `GEMINI.md` eliminado.
- [x] **F0.3** [V] `TASKS.md` creado y `Justfile` corregido (`TODO.md` → `TASKS.md`).
- [ ] **F0.4** [V] `requirements.txt`: separar runtime de desarrollo (`requirements-dev.txt`: djlint, pre-commit, prettier). Documentar en README.
- [ ] **F0.5** [R] README: retirar la tabla de credenciales con contraseña compartida. Reemplazar por "los datos de prueba viven en `03_dev_data.sql`" y, si se necesita, una nota de entorno local.
- [ ] **F0.6** [R] README: añadir sección **Origen y estado** ("v1 académica construida con asistencia de IA; v2 en curso: núcleo reescrito con tests"). Una línea honesta, sin dramatismo.
- [ ] **F0.7** [V] `.pre-commit-config.yaml`: agregar hook local de `just test` cuando F1.3 exista. Pintar con `pre-commit install`.
- [ ] **F0.8** [A] Revisión cruzada: la IA audita el árbol y reporta archivos muertos, imports sin uso y scripts sueltos. Yordy decide qué se elimina.

---

## F1 — Esquema y estrategia de datos

**Estado:** pendiente · **Estimación:** 14–18 h

**Objetivo:** que el autor pueda defender las 18 tablas y sus constraints, y que exista una base de test funcional. Es la fase más larga porque hoy no puede explicar casi nada.

**Criterio de salida:** tres ADR escritas por Yordy, esquema auditado tabla por tabla, `just test` ejecuta una suite real contra una base con el esquema cargado.

- [ ] **F1.1** [R] **ADR-0001 — Estrategia de acceso a datos.** Esqueleto en `docs/templates/adr.md`. Decidir SQL manual, ORM o híbrido *unmanaged*, con su costo explícito. Requisito del ramo: SQL manual para el núcleo.
- [ ] **F1.2** [R] **Auditoría del esquema, tabla por tabla.** Para cada una de las 18 tablas: qué representa, por qué existe, qué constraint la protege y qué regla de `docs/database/reglas.md` implementa. Validar las reglas en prosa (¿por qué 7 días? ¿por qué 30% VIP? ¿por qué 5 faltas?) contra `docs/requerimientos.md`.
- [ ] **F1.3** [R] **ADR-0002 — Estrategia de tests.** El problema: `manage.py test` crea la base de test desde las migraciones de Django, y las 7 apps tienen las migraciones vacías; el esquema vive en `01_schema.sql`. Sin resolver esto, ningún test puede correr. Opciones a evaluar: (a) fixture que carga `01_schema.sql`; (b) migrar el dominio a migraciones de Django; (c) modelos `managed = False` como espejo del esquema.
- [ ] **F1.4** [R] **ADR-0003 — Modelo de datos y normalización.** Qué se mantiene del esquema actual y qué cambia: tipos de dinero (`DECIMAL`), `UNIQUE` para sobrecupo, índices para las consultas de disponibilidad, `CHECK` de integridad horaria.
- [ ] **F1.5** [V] Aplicar los cambios aprobados en F1.4 a `01_schema.sql`, `entidades_atributos.md` y `diagram.dbml` en un mismo commit.
- [ ] **F1.6** [V] Implementar la estrategia de F1.3: fixture de esquema, `pytest-django` o `django.test.TestCase`, y un test trivial que pruebe la conexión y una tabla.
- [ ] **F1.7** [A] La IA escribe 10 preguntas de defensa sobre el modelo. Yordy las responde en voz alta, sin notas.

---

## F2 — Reserva atómica (el núcleo)

**Estado:** pendiente · **Estimación:** 12–16 h

**Objetivo:** eliminar la condición de carrera del flujo de reserva y demostrarlo con un test. Es el cambio que sostiene la historia de la entrevista.

**Criterio de salida:** dos reservas simultáneas del mismo bloque no pueden entrar; el test lo demuestra y corre en CI.

- [ ] **F2.1** [A] La IA documenta el bug actual en `docs/adr/0004-condicion-de-carrera.md` (esqueleto): chequeo `SELECT 1 …` y `INSERT` fuera de transacción, sin `UNIQUE`. Yordy describe el escenario de falla con sus palabras.
- [ ] **F2.2** [R] Definir el mecanismo: `UNIQUE (recurso, fecha, hora)` + transacción + manejo de `IntegrityError`. Escribir el test **antes** (rojo).
- [ ] **F2.3** [V] Implementar el mecanismo acordado. La plantilla y el mensaje de error son zona verde; la lógica, no.
- [ ] **F2.4** [R] Test de concurrencia real: dos hilos o dos conexiones compitiendo por el mismo bloque. Debe fallar contra `v1.0-academica`.
- [ ] **F2.5** [R] Revisar el cálculo de precio: `Decimal`, duración positiva, `hora_fin > hora`.
- [ ] **F2.6** [R] Reemplazar `except Exception: print(...)` por manejo tipado con `logging` y mensaje accionable.
- [ ] **F2.7** [A] Preguntas de defensa: ¿qué pasa si el usuario reintenta? ¿qué pasa si MySQL falla a mitad? ¿por qué `UNIQUE` y no un `SELECT … FOR UPDATE`?

---

## F3 — Cancelaciones y penalizaciones

**Estado:** pendiente · **Estimación:** 10–12 h

**Objetivo:** que las reglas de `reglas.md` existan en código y en tests, no solo en prosa.

**Criterio de salida:** las ventanas de cancelación, la progresión de multas y el bloqueo por reincidencia están cubiertos por tests.

- [ ] **F3.1** [R] Traducir a casos de prueba las reglas de cancelación (60 min normal, 30 min VIP/Socio), no-show y multa progresiva.
- [ ] **F3.2** [V] Implementar lo que Yordy especifique, con `Decimal` y transacción.
- [ ] **F3.3** [R] Bloqueo por 5 faltas vigentes y bloqueo por 3 intentos de login fallidos.
- [ ] **F3.4** [A] Casos borde: cancelación exactamente en el límite, reserva ya consumida, usuario duplicado en dos canchas el mismo bloque.

---

## F4 — Membresías y dinero

**Estado:** pendiente · **Estimación:** 8–10 h

**Objetivo:** que los descuentos y los montos sean verificables y no aproximados.

**Criterio de salida:** porcentajes validados entre 0 y 100, cálculo con `Decimal` y tests de redondeo.

- [ ] **F4.1** [R] Definir la regla de redondeo (CLP sin decimales) y su justificación.
- [ ] **F4.2** [R] Tests de descuento: 0 %, 15 %, 30 %, borde en 100 %.
- [ ] **F4.3** [V] Aplicar en vistas y plantillas; centralizar el formateo de moneda.
- [ ] **F4.4** [A] Revisión: buscar `float` y `round()` en el árbol y reportar cada uso.

---

## F5 — CI, deploy y demo

**Estado:** pendiente · **Estimación:** 10–12 h

**Objetivo:** que un revisor pueda ver el sistema funcionando sin instalar nada.

**Criterio de salida:** pipeline verde en cada push y URL pública con usuario demo.

- [ ] **F5.1** [V] GitHub Actions: servicio MySQL, `just db-reset`, `just test`, `djlint --check`.
- [ ] **F5.2** [V] Deploy con Docker (VPS, Railway o similar). Variables por entorno, sin credenciales en el repo.
- [ ] **F5.3** [R] Usuario demo de solo lectura con datos sembrados. Documentar el recorrido en 5 pasos.
- [ ] **F5.4** [V] README: sección de demo con URL, credenciales demo y capturas reales.

---

## F6 — Evidencia y caso de estudio

**Estado:** pendiente · **Estimación:** 8–10 h

**Objetivo:** convertir el repo en un argumento, no en un depósito de código.

**Criterio de salida:** `docs/caso-de-estudio.md` completo, README con sección Proceso, `ai-log.md` al día.

- [ ] **F6.1** [R] `docs/caso-de-estudio.md` desde `docs/templates/caso-de-estudio.md`. Se escribe aquí primero; el portfolio solo lo adapta.
- [ ] **F6.2** [R] README § Proceso: v1 académica, v2 reescrita, el bug de concurrencia encontrado y cómo se probó.
- [ ] **F6.3** [R] README § Decisiones: resumen de las ADR en una tabla, con enlace.
- [ ] **F6.4** [V] Capturas reales (no mockups) para README y para el portfolio.
- [ ] **F6.5** [A] Auditoría: ¿alguna afirmación del README no está respaldada por código o test? Reportar cada una.

---

## F7 — Defensa

**Estado:** pendiente · **Estimación:** 4 h

**Objetivo:** que ningún artefacto del repo esté por encima de lo que el autor puede explicar.

**Criterio de salida:** defensa grabada sin IA, sin notas y sin editor abierto.

- [ ] **F7.1** [A] Banco de 20 preguntas de defensa generado por la IA, ordenado por dificultad.
- [ ] **F7.2** [R] Responder en voz alta y grabar. Repetir hasta pasar las 20.
- [ ] **F7.3** [R] Modificación en vivo: agregar una regla de negocio nueva frente a cámara, siguiendo el flujo test → código.
- [ ] **F7.4** [R] Tag `v2.0` y release en GitHub. Recién aquí se desbloquea el portfolio.

---

## Fuera del alcance de v2.0

Presente en el esquema y en las reglas, pero no entra en esta release:

- Torneos, partidos y walkover.
- Widget del clima y consumo de API externa.
- Migración del frontend fuera de Bootstrap/jQuery.
- Panel analítico para administración.
- Recuperación de contraseña por correo.

## Backlog

- [ ] Revisar si `ConnectionDB` debe exponer un contexto transaccional uniforme.
- [ ] Cobertura de tests como métrica del README (solo si se puede medir de verdad).
- [ ] Revisar accesibilidad de las plantillas (Lighthouse ≥ 90), alineado con el estándar del portfolio.
