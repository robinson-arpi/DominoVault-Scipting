import os
import pandas as pd

# Declarar base_id y df como variables globales
base_id = 1
df = None  # Inicializamos df como None para que esté accesible globalmente

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

# def analizar_archivo(dpath_carpeta, carpeta_nombre, base_id):
#     archivo_csv = os.path.join(dpath_carpeta, "documents_info.csv")

#     if not os.path.isfile(archivo_csv):
#         print(f"No se encontró el archivo 'documents_info.csv' en {dpath_carpeta}.")
#         return

#     try:
#         # Lee el archivo CSV usando pandas con manejo de errores
#         df = pd.read_csv(archivo_csv, 
#                          on_bad_lines='skip',  # Ignorar líneas con errores
#                          quoting=3,             # Maneja comillas como texto plano
#                          delimiter=',')         # Asegúrate de usar el delimitador correcto

#         # Verifica si las columnas existen
#         if 'DocID' not in df.columns or 'FieldName' not in df.columns:
#             print(f"El archivo 'documents_info.csv' no contiene las columnas esperadas en {dpath_carpeta}.")
#             return

#         # Obtiene valores únicos
#         doc_ids_unicos = df['DocID'].nunique()
#         field_names_unicos = df['FieldName'].nunique()
#         field_names = df['FieldName'].unique()

#         print(f"En la carpeta '{carpeta_nombre}':")
#         print(f"Cantidad de DocID únicos: {doc_ids_unicos}")
#         print(f"Cantidad de FieldName únicos: {field_names_unicos}")

#         # Genera la consulta para insertar en la tabla Forms
#         query_forms = f"""
#         INSERT INTO Forms (id, name, base_id)
#         VALUES (DEFAULT, '{carpeta_nombre}', {base_id});
#         """
#         print(f"\nConsulta SQL para Forms:\n{query_forms}")

#         # Genera la consulta para crear la tabla con el nombre de la carpeta
#         query_create_table = f"CREATE TABLE {carpeta_nombre} (\n    id SERIAL PRIMARY KEY,"
#         for field in field_names:
#             query_create_table += f"\n    {field} VARCHAR(255),"
#         query_create_table = query_create_table.rstrip(',') + "\n);"

#         print(f"\nConsulta SQL para crear tabla '{carpeta_nombre}':\n{query_create_table}")
        
#     except Exception as e:
#         print(f"Ocurrió un error al analizar el archivo en {dpath_carpeta}: {e}")




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

        # Verifica si las columnas existen
        if 'DocID' not in df.columns or 'FieldName' not in df.columns:
            print(f"El archivo 'documents_info.csv' no contiene las columnas esperadas en {dpath_carpeta}.")
            return

        # Obtiene valores únicos y nombres de los campos
        doc_ids_unicos = df['DocID'].nunique()
        field_names_set = set(df['FieldName'].unique())
        field_names = list(field_names_set)

        print(f"En la carpeta '{carpeta_nombre}':")
        print(f"Cantidad de DocID únicos: {doc_ids_unicos}")
        print(f"Cantidad de FieldName únicos: {len(field_names)}")

        # Crear un DataFrame vacío con todas las columnas posibles
        transformed_data = pd.DataFrame(columns=field_names + ['DocID'])

        # Lista para almacenar las filas
        rows = []

        # Población del DataFrame
        for doc_id in df['DocID'].unique():
            doc_data = df[df['DocID'] == doc_id]
            # Crear una nueva fila con todos los campos
            new_row = {field: None for field in field_names}  # Inicializa todos los campos con None
            new_row['DocID'] = doc_id
            
            for _, row in doc_data.iterrows():
                new_row[row['FieldName']] = row.get('FieldValue', None)  # Asume que hay una columna 'FieldValue'
            
            # Añadir la nueva fila a la lista
            rows.append(new_row)

        # Crear el DataFrame final con todas las filas
        transformed_data = pd.concat([transformed_data, pd.DataFrame(rows)], ignore_index=True)

        # Reordenar columnas para que 'DocID' sea la primera
        columns_order = ['DocID'] + [col for col in transformed_data.columns if col != 'DocID']
        transformed_data = transformed_data[columns_order]
        # Reemplaza las comillas vacías dentro de cada celda
        transformed_data = transformed_data.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)
        # Eliminar columnas vacías (sin datos)
        transformed_data = transformed_data.dropna(axis=1, how='all')
        # Guardar los datos transformados en un nuevo archivo CSV
        output_csv = os.path.join(dpath_carpeta, "transformed_data.csv")
        transformed_data.to_csv(output_csv, index=False)
        print(f"Datos transformados guardados en '{output_csv}'.")

    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo en {dpath_carpeta}: {e}")

# Ejemplo de uso
dpath = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"
base_id = 1
listar_carpetas(dpath, base_id)