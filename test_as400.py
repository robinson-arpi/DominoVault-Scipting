import pyodbc
import const

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conn = pyodbc.connect(
                f"DRIVER={const.DRIVER};SYSTEM={const.HOST};DATABASE=SGSSD;UID={const.UID_DB};PWD={const.PWD_DB}"
            )
            print("Conexión exitosa")
        except pyodbc.Error as ex:
            print(f"Error al conectarse a la base de datos: {ex}")

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")

    def execute_select(self, query: str):
        """Ejecutar una consulta SELECT.
        Args:
            query (str): Query SQL de selección.
        Returns:
            list: Filas obtenidas de la consulta.
        """
        if not self.conn:
            print("No hay conexión establecida.")
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()  # Recuperar filas
            return rows
        except pyodbc.Error as ex:
            print(f"Error al ejecutar la consulta SELECT: {ex}")
            return None

    def execute_insert(self, query: str):
        """Ejecutar una consulta INSERT.
        Args:
            query (str): Query SQL de inserción.
        """
        if not self.conn:
            print("No hay conexión establecida.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()  # Confirmar cambios
            print("Inserción exitosa.")
        except pyodbc.Error as ex:
            print(f"Error al ejecutar la consulta INSERT: {ex}")

# Uso de la clase DatabaseManager
db_manager = DatabaseManager()

# Conectar a la base de datos
db_manager.connect()

# Ejemplo de un SELECT
select_query = "SELECT * FROM SGSSDB.PLACORD"
result = db_manager.execute_select(select_query)

# Mostrar los resultados del SELECT
if result:
    for row in result:
        print(row)

# Ejemplo de un INSERT
insert_query = "INSERT INTO SGSSDB.PLACORD (columna1, columna2) VALUES ('valor1', 'valor2')"
db_manager.execute_insert(insert_query)

# Cerrar la conexión
db_manager.close()
