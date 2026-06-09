# Arriendo Canchas - Sistema de Gestión Deportiva

Sistema integral para la administración de recintos deportivos, gestión de socios con membresías dinámicas, motor de reservas con prevención de sobrecupo y control de penalizaciones automáticas.

## Stack Tecnológico

- **Backend:** Django 6.x (Function-Based Views & SQL Manual)
- **Base de Datos:** MySQL 8.4
- **Frontend:** Bootstrap 5, jQuery 4 & SweetAlert2
- **Infraestructura:** Docker & Docker Compose
- **Automatización:** Justfile (Opcional)

---

## Guía de Instalación Rápida

Elige el método que mejor se adapte a tu entorno. En todos los casos, el sistema corre en **http://localhost:8000**.

### Capa 1: Uso de Justfile (Recomendado)

Requiere tener [Just](https://github.com/casey/just) instalado.

```bash
# 1. Configurar entorno (.env)
just setup

# 2. Levantar contenedores
just up

# 3. Inicializar base de datos y datos de prueba
just db-reset
```

### Capa 2: Uso de Docker Puro

Si no tienes Just instalado, usa los comandos nativos de Docker Compose.

```bash
# 1. Crear archivo de variables de entorno
cp .env.example .env

# 2. Levantar la infraestructura
docker compose up -d --build

# 3. Restaurar Base de Datos (Esperar 10s a que el motor inicie)
docker compose exec -T db mysql -u admin -psecret arriendo_db -e "source /docker-entrypoint-initdb.d/01_schema.sql"
docker compose exec -T db mysql -u admin -psecret arriendo_db -e "source /docker-entrypoint-initdb.d/02_master_data.sql"
docker compose exec -T db mysql -u admin -psecret arriendo_db -e "source /docker-entrypoint-initdb.d/03_dev_data.sql"

# 4. Aplicar migraciones internas de Django
docker compose exec app python manage.py migrate
```

### Capa 3: Instalación Local (Python + XAMPP)

Si prefieres ejecutar el código directamente en tu máquina sin usar Docker:

```bash
# 1. Base de Datos (XAMPP / Laragon)
# - Crea una base de datos llamada 'arriendo_db' en tu gestor MySQL.
# - Ejecuta los 3 scripts SQL en orden:
#   1. src/database/sql/01_schema.sql
#   2. src/database/sql/02_master_data.sql
#   3. src/database/sql/03_dev_data.sql

# 2. Configurar Entorno
cp .env.example .env
# Ajusta DB_HOST=localhost y DB_PORT=3306 en tu .env

# 3. Instalar Dependencias
pip install -r requirements.txt

# 4. Iniciar Servidor
python manage.py runserver
```

---

## Credenciales de Acceso (Pruebas)

Todas las cuentas de prueba comparten la contraseña: `0000`

| Rol               | Usuario (RUT)  | Características                              |
| :---------------- | :------------- | :------------------------------------------- |
| **Administrador** | `11.111.111-1` | Gestión total de usuarios e infraestructura. |
| **Recepcionista** | `17.744.333-2` | Gestión de reservas y registro de No-show.   |
| **Cliente VIP**   | `22.222.222-2` | Aplica 15% de descuento en reservas.         |
| **Cliente Socio** | `33.333.333-3` | Aplica 30% de descuento en reservas.         |

---

## Documentación del Proyecto

El respaldo técnico detallado se encuentra en la carpeta `/docs`:

- **Arquitectura:** [Estructura de Apps y Estándares](./docs/arquitectura.md)
- **Base de Datos:** [Diagramas y Diccionario de Datos](./docs/database/README.md)
- **Negocio:** [Reglas y Requerimientos Funcionales](./docs/requerimientos.md)
- **Evaluación:** [Requerimientos de la Evaluación Sumativa](./docs/ev03_requirements.md)

---

Developed by IPVG Students - 2026
