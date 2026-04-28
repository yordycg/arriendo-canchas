# Arriendo Canchas

Sistema integral para la gestión de arriendo de canchas, quinchos, organización de torneos y administración de socios. Este proyecto está diseñado con un enfoque en la integridad de datos y la automatización de políticas de negocio.

## Características Principales

- **Gestión de Reservas:** Sistema inteligente para canchas y quinchos con prevención de sobrecupo.
- **Membresías Progresivas:** Categorización de usuarios (Normal, VIP, Socio) con beneficios dinámicos.
- **Sistema de Penalizaciones:** Control automático de inasistencias (No-show) y bloqueos por reincidencia.
- **Módulo de Torneos:** Gestión de ligas, equipos (incluyendo invitados) y resultados con reglas de Walkover (W.O.).
- **Infraestructura Dockerizada:** Entorno de desarrollo consistente y listo para usar.

## Stack Tecnológico

- **Backend:** Python / Django (en proceso)
- **Base de Datos:** MySQL 8.0
- **Infraestructura:** Docker / Docker Compose
- **Documentación:** DBML, Diagramas SVG y Markdown

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <tu-url-de-github>
cd arriendo-canchas
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta tus credenciales:

```bash
cp .env.example .env
```

### 3. Levantar la infraestructura

Asegúrate de tener Docker instalado y ejecuta:

```bash
docker-compose up -d
```

### 4. Inicializar la Base de Datos

Puedes usar tu herramienta favorita para ejecutar los scripts en orden:

1. `database/sql/01_schema.sql` (Esquema)
2. `database/sql/02_master_data.sql` (Datos obligatorios)
3. `database/sql/03_dev_data.sql` (Datos de prueba)

## Documentación del Diseño

Para más detalles sobre la estructura de la base de datos, reglas de negocio y políticas, consulta la carpeta `/docs/database`:

- [Reglas de Negocio](./docs/database/reglas.md)
- [Políticas de Membresía y Penalización](./docs/database/politicas.md)
- [Diccionario de Datos](./docs/database/entidades_atributos.md)
- [Diagrama Entidad-Relación](./docs/database/arriendo_canchas_db.svg)

---
