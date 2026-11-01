# AGENTS.md — arriendo-canchas

> Fuente única de instrucciones para agentes de IA (opencode, pi, agy, Claude, Codex, Gemini).
> Reemplaza a `GEMINI.md`, que fue eliminado para evitar dos fuentes de verdad.

---

## 1. Contexto del autor

Yordy Carmona, estudiante de tercer año de Ingeniería en Informática, perfil backend Python/Django.

Este repositorio nació como proyecto académico y **fue construido en gran parte con asistencia de IA**. La consecuencia es concreta: hoy el autor no puede defender la mayoría del código. Por eso la misión de las próximas semanas **no es agregar funcionalidades, sino apropiarse del núcleo**: entenderlo, reescribirlo y demostrarlo con tests.

Cómo tratarlo:

- Prefiere una respuesta lenta y explicada a una rápida que no entienda.
- No asumas que entiende algo porque el código exista.
- Cuando pida un artefacto de zona roja, entrega **solo el esqueleto con preguntas** (§4).
- Si detectas que su explicación es incorrecta, corrígelo antes de seguir escribiendo código.

---

## 2. Stack y convenciones

- **Lenguaje:** Python 3.12+ · **Framework:** Django 6.0.x
- **Base de datos:** MySQL 8.x · driver **PyMySQL** (monkey-patched como `MySQLdb`)
- **Frontend:** Bootstrap 5 + jQuery · **Infra:** Docker Compose · **Runner:** Just
- **Capa de datos:** SQL manual vía `ConnectionDB`. El ORM de Django se usa solo para tareas internas del framework. Esta decisión está en revisión: ver `docs/adr/0001-estrategia-de-datos.md`.
- **Nombres de dominio en español** (`reservas_canchas`, `contador_faltas`), consistente con el esquema. Infraestructura y configuración en inglés (`compose.yaml`, `settings.py`).
- **PEP 8**, type hints en funciones públicas y docstrings en clases y métodos no triviales.
- **Dinero:** siempre `Decimal`, nunca `float`.
- **Errores:** `logging`, nunca `print`. Prohibido `except Exception` sin tipo y sin relanzar o registrar con contexto.
- **Transacciones:** toda operación que lea y luego escriba debe declarar su límite transaccional de forma explícita.

### Comandos

| Comando | Qué hace |
|---|---|
| `just setup` | Crea `.env`, `.venv` e instala dependencias |
| `just up` | Levanta app + base de datos |
| `just db-reset` | Recrea la base desde los tres scripts SQL |
| `just py <cmd>` | Ejecuta un comando de Django dentro del contenedor |
| `just lint` | djlint + prettier en modo verificación |
| `just test [args]` | Suite de tests (hoy vacía; ver F1.3) |
| `just check` | `lint` + `test` — debe pasar antes de cada commit |

---

## 3. Git

- **Conventional Commits obligatorio:** `<type>(<scope>): <description>`.
  Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `build`, `ci`.
  Scopes: `bookings`, `courts`, `users`, `auth`, `memberships`, `penalties`, `db`, `infra`, `docs`.
- **Ramas:** `feature/<tema>` desde `develop`; se integra a `develop` por PR. `main` solo recibe releases con tag.
- **Commits atómicos.** Un commit gigante generado de una vez está prohibido: si un cambio toca esquema, vista y plantilla, son tres commits.
- **Cuerpo del commit con el por qué.** La descripción dice qué cambió; el cuerpo dice por qué y qué se descartó. Plantilla en `docs/templates/commit.md`.
- **Si cambia el esquema,** el mismo commit actualiza `src/database/sql/01_schema.sql`, `docs/database/entidades_atributos.md` y `docs/database/diagram.dbml`.
- **Nunca** commitear `.env`, credenciales reales ni datos personales.

---

## 4. Regla de propiedad (no negociable)

El objetivo de cada tarea es que el autor pueda defenderla. Por eso el trabajo se divide en zonas.

### Zona roja — no la escribas

- El esquema y las reglas de negocio.
- Autenticación, sesión y autorización por rol.
- Las **aserciones** de los tests (el andamiaje sí; qué se afirma, no).
- Los ADR y la sección de decisiones del README.
- El caso de estudio.

Si te piden código de zona roja: **no lo escribas**. Haz preguntas hasta que el autor lo escriba, y después revísalo. Puedes corregir ortografía, formato y consistencia.

### Zona verde — escríbela sin pedir permiso

Plantillas HTML, CSS, Dockerfile y compose, CI, seeds, fixtures, renombres, migraciones mecánicas, formateo, documentación de instalación.

### Zona azul — uso obligatorio

Revisar el diff del autor, proponer casos borde, escribir tests que **fallen** para que él los haga pasar, explicar un archivo línea por línea, y hacer preguntas de defensa antes de cerrar la sesión.

### Reglas de verificación

- **Regla de reescritura:** no se commitea código que el autor no pueda reescribir desde cero en un archivo vacío. Si no puede, se borra y se rehace.
- **Regla de los 60 segundos:** antes de cada commit, el autor explica el diff en voz alta. Si se traba, el commit no se hace.

---

## 5. Gate de sesión

Al cerrar cada sesión de trabajo:

1. Pide al autor que explique el diff en voz alta, sin mirar el editor.
2. Hazle **una** pregunta de defensa sobre la parte más difícil del cambio.
3. Registra la sesión en `docs/ai-log.md`: qué se delegó, qué escribió él, qué se reescribió.

Si no puede responder, la tarea queda abierta. No la marques como terminada.

---

## 6. Definición de terminado

Una tarea está terminada cuando:

1. Existió un test que fallaba antes del cambio y pasa después (salvo que la tarea sea puramente documental).
2. `just check` pasa.
3. El esquema y sus documentos están sincronizados, si aplica.
4. No hay `print`, `except` desnudo ni `float` para dinero.
5. Las operaciones leer-y-escribir tienen límite transaccional explícito.
6. Hay commit convencional y atómico, con el por qué en el cuerpo.
7. El autor puede explicarlo en 60 segundos y modificarlo en vivo.

---

## 7. Prohibiciones

- Generar el README, los ADR o el caso de estudio sin que el autor dicte las decisiones.
- Commitear o pushear sin que el autor haya explicado el diff.
- Inventar métricas, capturas, usuarios o funcionalidades no implementadas.
- Reescribir un archivo completo cuando se pidió un cambio puntual.
- Agregar dependencias sin justificarlas contra la regla del stack.
- Tocar `main` salvo para un release con tag.
- "Arreglar" refactorizando el núcleo sin que se haya pedido.
- Dejar archivos temporales, scripts sueltos o andamiaje de agente en el árbol público.

---

## 8. Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `TASKS.md` | Estado, fases y próximos pasos. Fuente de verdad del trabajo. |
| `docs/adr/` | Decisiones de arquitectura, escritas por el autor. |
| `docs/templates/` | Esqueletos con preguntas. No se completan con IA. |
| `docs/ai-log.md` | Registro de uso de IA por sesión. |
| `docs/caso-de-estudio.md` | Evidencia pública del proyecto. |
| `docs/database/` | Reglas de negocio, entidades, relaciones y diagrama. |
| `src/database/sql/` | Esquema y semillas. |
| `README.md` | Cara pública: problema, stack, cómo correr, proceso. |
