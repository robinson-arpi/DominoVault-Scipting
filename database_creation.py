import os
os.add_dll_directory('C:\\Program Files\\IBM\\IBM DATA SERVER DRIVER\\bin')


import ibm_db

# Parámetros de conexión
dsn = (
    "DATABASE=testdb;"
    "HOSTNAME=localhost;"  # Cambia esto por la IP de tu contenedor si es diferente
    "PORT=50000;"
    "PROTOCOL=TCPIP;"
    "UID=db2inst1;"       # Usuario de la base de datos
    "PWD=password;"       # Contraseña del usuario
)

# Conectar a la base de datos DB2
try:
    conn = ibm_db.connect(dsn, "", "")
    print("Conexión exitosa a la base de datos DB2.")

    # Crear las tablas
    create_databases_table = """
    CREATE TABLE DataBases (
        id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
    );
    """
    
    create_forms_table = """
    CREATE TABLE Forms (
        id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        base_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY (base_id) REFERENCES DataBases(id)
    );
    """
    
    # Ejecutar las sentencias SQL para crear las tablas
    ibm_db.exec_immediate(conn, create_databases_table)
    ibm_db.exec_immediate(conn, create_forms_table)
    print("Tablas creadas exitosamente.")

except Exception as e:
    print(f"Error al conectar a la base de datos o crear tablas: {e}")

finally:
    # Cerrar la conexión
    if conn:
        ibm_db.close(conn)
        print("Conexión cerrada.")
