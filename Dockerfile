FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para MySQL y compilación
RUN apt-get update && apt-get install -y --no-install-recommends     gcc     default-libmysqlclient-dev     pkg-config     curl     && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El código se montará como volumen en desarrollo, pero copiamos por seguridad
COPY . .

# Comando por defecto para desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
