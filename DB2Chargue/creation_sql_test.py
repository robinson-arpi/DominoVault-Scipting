import os
import pandas as pd

def listar_carpetas(dpath, base_id):
    try:
        # Verifica si el directorio existe
        if not os.path.exists(dpath):
            print(f"El directorio '{dpath}' no existe.")
            return
        
        # Verifica si es un directorio
        if not os.path.isdir(dpath):
            print(f"'{dpath}' no es un directorio.")
            return

        # Lista todas las carpetas en el directorio
        carpetas = [nombre for nombre in os.listdir(dpath) if os.path.isdir(os.path.join(dpath, nombre))]
        
        if carpetas:
            print("Carpetas encontradas:")
            for carpeta in carpetas:
                print(f"\n- {carpeta}")
                analizar_archivo(os.path.join(dpath, carpeta), carpeta, base_id)
        else:
            print("No se encontraron carpetas.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

def analizar_archivo(dpath_carpeta, carpeta_nombre, base_id):
    archivo_csv = os.path.join(dpath_carpeta, "documents_info.csv")

    if not os.path.isfile(archivo_csv):
        print(f"No se encontró el archivo 'documents_info.csv' en {dpath_carpeta}.")
        return

    try:
        # Lee el archivo CSV usando pandas con manejo de errores
        df = pd.read_csv(archivo_csv, 
                         on_bad_lines='skip',  # Ignorar líneas con errores
                         quoting=3,             # Maneja comillas como texto plano
                         delimiter=',')         # Asegúrate de usar el delimitador correcto

        # Verifica si las columnas 'DocID' y 'FieldName' existen
        if 'DocID' not in df.columns or 'FieldName' not in df.columns:
            print(f"El archivo 'documents_info.csv' no contiene las columnas esperadas en {dpath_carpeta}.")
            return

        # Obtiene valores únicos de DocID y FieldName
        doc_ids_unicos = df['DocID'].nunique()
        field_names_unicos = df['FieldName'].nunique()
        field_names = df['FieldName'].unique()

        print(f"En la carpeta '{carpeta_nombre}':")
        print(f"Cantidad de DocID únicos: {doc_ids_unicos}")
        print(f"Cantidad de FieldName únicos: {field_names_unicos}")

        # Genera la consulta para insertar en la tabla Forms
        query_forms = f"""
        INSERT INTO Forms (id, name, base_id)
        VALUES (DEFAULT, '{carpeta_nombre}', {base_id});
        """
        print(f"\nConsulta SQL para Forms:\n{query_forms}")

        # Genera la consulta para crear la tabla con el nombre de la carpeta
        query_create_table = f"CREATE TABLE {carpeta_nombre} (\n    id SERIAL PRIMARY KEY,"
        
        # Itera sobre los FieldNames y calcula la longitud máxima de los valores asociados a cada campo
        for field in field_names:
            # Filtra las filas correspondientes a este FieldName
            valores = df[df['FieldName'] == field]['DocID'].astype(str)
            
            # Obtén la longitud máxima de los valores en la columna 'DocID' para este campo
            max_length = valores.apply(len).max()  # Calcula la longitud máxima de los valores
            max_length = max(1, max_length)  # Asegúrate de que la longitud sea al menos 1
                
            # Agrega la columna a la consulta SQL con el tamaño adecuado
            query_create_table += f"\n    {field} VARCHAR({max_length}),"
        
        query_create_table = query_create_table.rstrip(',') + "\n);"

        print(f"\nConsulta SQL para crear tabla '{carpeta_nombre}':\n{query_create_table}")
        
    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo en {dpath_carpeta}: {e}")

# Ejemplo de uso
dpath = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"
base_id = 1
listar_carpetas(dpath, base_id)
