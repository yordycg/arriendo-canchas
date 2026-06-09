# Justfile - Command Runner for Arriendo Canchas (Container Edition)
set dotenv-load := true

# Database Variables
DB_NAME := env_var_or_default('DB_NAME', 'arriendo_db')
DB_USER := env_var_or_default('DB_USER', 'admin')
DB_PASS := env_var_or_default('DB_PASS', 'secret')

# List all available commands
default:
    @just --list

# --- SETUP & INSTALLATION ---

# Inicializa el entorno (Copia env, crea venv local para LSP)
setup:
    [ -f .env ] || cp .env.example .env
    direnv allow .
    [ -d .venv ] || python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    @echo "✅ Entorno local listo."

# --- INFRASTRUCTURE (Docker) ---

# Levanta todo el entorno (App + DB) y muestra logs
up:
    docker compose up -d --build
    docker compose logs -f

# Detiene la infraestructura
down:
    docker compose down

# Ver logs en tiempo real
logs:
    docker compose logs -f

# --- DJANGO DEVELOPMENT (Inside Container) ---

# Ejecuta cualquier comando de Python/Django (Ej: just py manage.py migrate)
py *args:
    docker compose exec app python {{args}}

# Crea una nueva aplicación con permisos de usuario correctos
startapp name:
    @echo "🛠️ Creando aplicación '{{name}}'..."
    @docker compose exec app python manage.py startapp {{name}} src/{{name}}
    @sudo chown -R $(id -u):$(id -g) src/{{name}}
    @echo "✅ Aplicación '{{name}}' creada exitosamente en src/{{name}}."

# --- DATABASE MANAGEMENT ---

# Reseteo total: Borra, recrea y carga todos los datos desde archivos montados
db-reset:
    @echo "🚀 Iniciando reseteo completo de la base de datos..."
    @docker compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} -e "DROP DATABASE IF EXISTS {{DB_NAME}}; CREATE DATABASE {{DB_NAME}} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    @echo "📜 Aplicando esquema manual (01_schema.sql)..."
    @docker compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/01_schema.sql"
    @echo "⚙️ Cargando datos maestros (02_master_data.sql)..."
    @docker compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/02_master_data.sql"
    @echo "🧪 Cargando datos de prueba (03_dev_data.sql)..."
    @docker compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /docker-entrypoint-initdb.d/03_dev_data.sql"
    @echo "📦 Django: Ejecutando migraciones pendientes..."
    @just py manage.py migrate --noinput
    @echo "✅ Base de datos restaurada."

# --- QUALITY & CLEANUP ---

# Formatea el código
format:
    @docker compose exec app djlint . --reformat --indent 2 --ignore "H021,H030,H031,D018"
    @npx prettier --write "**/static/**/*.{js,css}" "README.md" "TODO.md"
