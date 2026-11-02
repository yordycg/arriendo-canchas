# Justfile - Command Runner for Arriendo Canchas (Container Edition)
set dotenv-load := true

# --- ENTORNO LOCAL ---
# Gestor de contenedores: podman si está disponible, docker si no.
# Forzar uno explícito: COMPOSE=docker just up
COMPOSE := env_var_or_default('COMPOSE', `command -v podman >/dev/null 2>&1 && echo podman || echo docker`)
# Entorno virtual del host, creado por `just setup`. Solo se usa para lint, nunca para ejecutar la app.
VENV := env_var_or_default('VENV', '.venv')
DJLINT := VENV + '/bin/djlint'

# Database Variables
DB_NAME := env_var_or_default('DB_NAME', 'arriendo_db')
DB_USER := env_var_or_default('DB_USER', 'admin')
DB_PASS := env_var_or_default('DB_PASS', 'secret')

# List all available commands
default:
    @just --list

# --- SETUP & INSTALLATION ---

# Crea .env, el venv local y las dependencias de runtime + desarrollo
setup:
    [ -f .env ] || cp .env.example .env
    [ -d {{VENV}} ] || python3 -m venv {{VENV}}
    {{VENV}}/bin/pip install -r requirements-dev.txt
    @command -v direnv >/dev/null && direnv allow . || echo "direnv no está instalado: activa el venv a mano."
    @echo "✅ Entorno local listo. Si direnv ya estaba activo, ejecuta: direnv reload"

# --- INFRASTRUCTURE (Containers) ---

# Levanta todo el entorno (App + DB) y muestra logs
up:
    {{COMPOSE}} compose up -d --build
    {{COMPOSE}} compose logs -f

# Detiene la infraestructura
down:
    {{COMPOSE}} compose down

# Ver logs en tiempo real
logs:
    {{COMPOSE}} compose logs -f

# --- DJANGO DEVELOPMENT (Inside Container) ---

# Ejecuta cualquier comando de Python/Django (Ej: just py manage.py migrate)
py *args:
    {{COMPOSE}} compose exec app python {{args}}

# Crea una nueva aplicación con permisos de usuario correctos
startapp name:
    @echo "🛠️ Creando aplicación '{{name}}'..."
    @{{COMPOSE}} compose exec app python manage.py startapp {{name}} src/{{name}}
    @sudo chown -R $(id -u):$(id -g) src/{{name}}
    @echo "✅ Aplicación '{{name}}' creada exitosamente en src/{{name}}."

# --- DATABASE MANAGEMENT ---

# Reseteo total: Borra, recrea y carga todos los datos desde archivos montados
db-reset:
    @echo "🚀 Iniciando reseteo completo de la base de datos..."
    @{{COMPOSE}} compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} -e "DROP DATABASE IF EXISTS {{DB_NAME}}; CREATE DATABASE {{DB_NAME}} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    @echo "📜 Aplicando esquema manual (01_schema.sql)..."
    @{{COMPOSE}} compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/01_schema.sql"
    @echo "⚙️ Cargando datos maestros (02_master_data.sql)..."
    @{{COMPOSE}} compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/02_master_data.sql"
    @echo "🧪 Cargando datos de prueba (03_dev_data.sql)..."
    @{{COMPOSE}} compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/03_dev_data.sql"
    @echo "📦 Django: Ejecutando migraciones pendientes..."
    @just py manage.py migrate --noinput
    @echo "✅ Base de datos restaurada."

# --- QUALITY (host) ---

# Formatea plantillas, estilos y documentación (no requiere contenedor)
format:
    @[ -x {{DJLINT}} ] || { echo "Falta {{VENV}}. Ejecuta: just setup"; exit 1; }
    {{DJLINT}} . --reformat --indent 2 --ignore "H021,H030,H031,D018"
    npx prettier --write "**/static/**/*.{js,css}" "README.md" "TASKS.md"

# Verifica formato sin modificar archivos (no requiere contenedor)
lint:
    @[ -x {{DJLINT}} ] || { echo "Falta {{VENV}}. Ejecuta: just setup"; exit 1; }
    {{DJLINT}} . --check --indent 2 --ignore "H021,H030,H031,D018"
    npx prettier --check "**/static/**/*.{js,css}" "README.md" "TASKS.md"

# Ejecuta la suite de tests dentro del contenedor (vacía hasta cerrar F1.3)
test *args:
    @{{COMPOSE}} compose exec app true 2>/dev/null || { echo "El contenedor no está corriendo. Ejecuta: just up"; exit 1; }
    {{COMPOSE}} compose exec app python manage.py test {{args}}

# Gate previo a commit: lint (host) + tests (contenedor)
check: lint test
