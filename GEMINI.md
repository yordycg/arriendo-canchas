# Gemini Project Context & Mandates

Este archivo contiene las instrucciones fundacionales para el agente Gemini CLI en el proyecto **Arriendo Canchas**. Estas reglas tienen precedencia sobre cualquier comportamiento por defecto.

## 🎯 Contexto del Proyecto
Sistema de gestión deportiva para arriendo de canchas y quinchos, con un fuerte enfoque en políticas de membresía (Normal, VIP, Socio) y penalizaciones automáticas.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.12+ (Actual: 3.14+)
- **Framework Backend:** Django 6.0.x
- **Base de Datos:**
  - Motor: MySQL 8.x / 9.x
  - Driver: **PyMySQL** (Monkey-patched as MySQLdb)
- **Frontend:**
  - Framework CSS: **Bootstrap 5**
  - Librería JS: **jQuery**
- **Infraestructura:** Docker & Docker Compose
- **Entorno Virtual:** .venv (venv)

## 📜 Reglas de Desarrollo

### 1. Frontend & UI
- **Estilo:** Priorizar el uso de clases nativas de Bootstrap 5 para el diseño.
- **Interactividad:** Usar jQuery para manipulaciones del DOM y peticiones AJAX sencillas según requerimiento del curso.
- **Limpieza:** Mantener el CSS personalizado en archivos separados, evitando estilos en línea.

### 1. Git & Commits
- **Convención:** Usar estrictamente **Conventional Commits**.
  - `feat:` para nuevas funcionalidades.
  - `fix:` para correcciones de errores.
  - `docs:` para cambios en documentación.
  - `infra:` para cambios en Docker o configuración de entorno.
  - `db:` para cambios en esquemas o semillas SQL.
- **Ramas:** 
  - `main`: Solo para versiones estables y producción.
  - `develop`: Rama principal de integración y desarrollo.
  - `feature/nombre-tarea`: Las nuevas funcionalidades o apps DEBEN desarrollarse en ramas independientes y luego integrarse a `develop` mediante un Pull Request o merge.

### 2. Base de Datos
- **Sincronización:** Cualquier cambio en `database/sql/01_schema.sql` DEBE ser reflejado inmediatamente en:
  - `docs/database/entidades_atributos.md`
  - `docs/database/diagram.dbml`
- **Integridad:** Mantener siempre los `CHECK` constraints para reglas de negocio críticas.

### 3. Estilo de Código (Python/Django)
- Seguir **PEP 8**.
- **Capa de Datos:** Se utilizará **SQL Manual** a través de la clase `ConnectionDB` (`pymysql`) para todas las operaciones de base de datos, omitiendo el uso del ORM de Django para el núcleo de la lógica de negocio.
- Usar **Type Hints** en todas las funciones y métodos.
- Documentar clases y métodos complejos con Docstrings.

## 🤖 Instrucciones para el Agente
- **Investigación:** Antes de proponer un cambio, analiza:
  - Las reglas de negocio en `docs/database/reglas.md`.
  - La especificación funcional en `docs/requerimientos.md`.
  - La estructura definida en `docs/arquitectura.md`.
- **Validación:** Siempre que se agregue una funcionalidad, proponer o crear el test unitario correspondiente.
- **Brevidad:** Mantener las explicaciones técnicas directas y concisas.
