import pyodbc
from config import constants as const
class DBConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conn = pyodbc.connect(
                f"DRIVER={const.DRIVER};SYSTEM={const.HOST};DATABASE={const.DATABASE};UID={const.UID_DB};PWD={const.PWD_DB}"
            )
            print("Conexión exitosa")
        except pyodbc.Error as ex:
            print(f"Error al conectarse a la base de datos: {ex}")

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")

    def get_connection(self):
        """Devuelve la conexión actual."""
        if self.conn:
            return self.conn
        else:
            print("No hay conexión establecida.")
            return None
