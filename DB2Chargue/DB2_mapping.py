import  os
import sys
# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB2Chargue.db.queries import DatabaseManager


# Inicializar el administrador de la base de datos
db_manager = DatabaseManager()
# Cerrar conexión
db_manager.db_connection.close()