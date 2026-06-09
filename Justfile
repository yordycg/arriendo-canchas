# Justfile - Command Runner for Arriendo Canchas (Container Edition)
set dotenv-load := true

# Database Variables
DB_NAME := env_var_or_default('DB_NAME', 'arriendo_db')
DB_USER := env_var_or_default('DB_USER', 'root')
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
    @echo "✅ Entorno local listo para Neovim/LSP."

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

# --- DATABASE MANAGEMENT ---

# Reseteo total: Borra, recrea y carga todos los datos (Dentro del contenedor)
db-reset:
    @echo "🚀 Iniciando reseteo completo de la base de datos..."
    @docker compose exec -T db mysql --default-character-set=utf8mb4 -u{{DB_USER}} -p{{DB_PASS}} -e "DROP DATABASE IF EXISTS {{DB_NAME}}; CREATE DATABASE {{DB_NAME}} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    @echo "📜 Aplicando esquema manual (01_schema.sql)..."
    @docker cp src/database/sql/01_schema.sql arriendo-canchas-db:/tmp/01_schema.sql
    @docker compose exec -T db mysql --default-character-set=utf8mb4 -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /tmp/01_schema.sql"
    @echo "⚙️ Cargando datos maestros (02_master_data.sql)..."
    @docker cp src/database/sql/02_master_data.sql arriendo-canchas-db:/tmp/02_master_data.sql
    @docker compose exec -T db mysql --default-character-set=utf8mb4 -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /tmp/02_master_data.sql"
    @echo "🧪 Cargando datos de prueba (03_dev_data.sql)..."
    @docker cp src/database/sql/03_dev_data.sql arriendo-canchas-db:/tmp/03_dev_data.sql
    @docker compose exec -T db mysql --default-character-set=utf8mb4 -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} -e "source /tmp/03_dev_data.sql"
    @echo "📦 Django: Ejecutando migraciones pendientes..."
    @docker compose exec app python manage.py migrate --noinput
    @echo "✅ Base de datos lista."

# Entrar a la terminal de MySQL
db-shell:
    docker compose exec db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}}

# --- DJANGO DEVELOPMENT (Inside Container) ---

# Crea una nueva aplicación con permisos de usuario correctos
startapp name:
    @echo "🛠️ Creando aplicación '{{name}}'..."
    docker compose exec app python manage.py startapp {{name}} src/{{name}}
    sudo chown -R $(id -u):$(id -g) src/{{name}}
    @echo "✅ Aplicación '{{name}}' creada exitosamente en src/{{name}}."

# Crea nuevas migraciones basadas en los modelos
mm:
    docker compose exec app python manage.py makemigrations

# Aplica las migraciones a la DB
migrate:
    docker compose exec app python manage.py migrate

# Entra a la shell de Django
shell:
    docker compose exec app python manage.py shell

# Entra a la terminal del contenedor Django
bash:
    docker compose exec app bash

# --- QUALITY & CLEANUP ---

# Formatea el código
format:
    @docker compose exec app djlint . --reformat --indent 2 --ignore "H021,H030,H031,D018"
    @npx prettier --write "**/static/**/*.{js,css}" "README.md" "TODO.md"
