import pymysql
from django.conf import settings


class DatabaseManager:
    def get_connection(self):
        return pymysql.connect(
            host=settings.DB_CONFIG["HOST"],
            user=settings.DB_CONFIG["USER"],
            password=settings.DB_CONFIG["PASSWORD"],
            database=settings.DB_CONFIG["NAME"],
            port=settings.DB_CONFIG["PORT"],
            charset='utf8mb4',
            # Mecanismo que permite ir fila x fila...
            # DictCursor: retorna los datos como diccionarios de python.
            cursorclass=pymysql.cursors.DictCursor,
        )

    def execute(self, query, params=None):
        """Ejecutar una sola query."""
        # Conectarse a la db de mysql
        connection = self.get_connection()
        cursor = connection.cursor()

        # Procedimiento dentro de la db...
        cursor.execute(query, params)
        connection.commit()

        # Cerrar conexion de mysql
        cursor.close()
        connection.close()

    def exists(self, query, params=None):
        """Verificar si un registro existe."""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)
        # Otener solo la 1era fila, y ya saber si existe un registro asociado.
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        # Retornar el resultado sino esta vacio.
        return result is not None

    def get_all(self, query, params=None):
        """Retorna todas la filas."""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)
        # Obtener todos los datos...
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    def get_one(self, query, params=None):
        """Retornar un registro."""
        connection  = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(query, params)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result
