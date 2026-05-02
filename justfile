# Justfile - Command Runner for Arriendo Canchas
# Multi-OS compatible (Windows/Linux/macOS)

set dotenv-load := true
set shell := ["powershell", "-Command"]

DB_NAME := env_var('DB_NAME')
DB_USER := env_var('DB_USER')
DB_PASS := env_var('DB_PASS')

# List all available commands
default:
    @just --list

# --- INFRASTRUCTURE (Docker) ---

# Start the MySQL database container
db-up:
    docker-compose up -d db

# Stop the MySQL database container
db-down:
    docker-compose stop db

# View database logs
db-logs:
    docker-compose logs -f db

# --- DATABASE MANAGEMENT ---

# Full DB reset: drops, recreates and seeds the database
db-reset:
    @echo "Resetting database '{{DB_NAME}}'..."
    @docker-compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} -e "DROP DATABASE IF EXISTS {{DB_NAME}}; CREATE DATABASE {{DB_NAME}};"
    @echo "Applying schema (01)..."
    @docker-compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} < database/sql/01_schema.sql
    @echo "Loading master data (02)..."
    @docker-compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} < database/sql/02_master_data.sql
    @echo "Loading development data (03)..."
    @docker-compose exec -T db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}} < database/sql/03_dev_data.sql
    @echo "Database successfully reloaded."

# Access the MySQL shell inside the container
db-shell:
    docker-compose exec db mysql -u{{DB_USER}} -p{{DB_PASS}} {{DB_NAME}}

# --- DEVELOPMENT (Django Local) ---

# Run the Django development server locally
run:
    python manage.py runserver

# Open the Django shell
shell:
    python manage.py shell

# --- QUALITY, FORMATTING & CLEANUP ---

# Format all files using the right tool for each type
format:
    @echo "Formatting HTML with djlint..."
    @djlint . --reformat --indent 2
    @echo "Formatting JS/CSS with prettier..."
    @npx prettier --write "**/static/**/*.{js,css}" "README.md" "TODO.md"

# Clean Python cache and temporary files
clean:
    @echo "Cleaning Python cache files..."
    @python -c "import pathlib, shutil; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
    @echo "Cleanup complete."
