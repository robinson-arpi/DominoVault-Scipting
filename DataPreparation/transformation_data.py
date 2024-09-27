import os
import pandas as pd
import re

def verificar_directorio(path):
    """Verifica si el path existe y es un directorio."""
    if not os.path.exists(path):
        print(f"El directorio '{path}' no existe.")
        return False
    if not os.path.isdir(path):
        print(f"'{path}' no es un directorio.")
        return False
    return True

def listar_carpetas(dpath):
    """Lista las carpetas en un directorio dado y analiza los archivos dentro de ellas."""
    if not verificar_directorio(dpath):
        return
    
    carpetas = [nombre for nombre in os.listdir(dpath) if os.path.isdir(os.path.join(dpath, nombre))]
    
    if carpetas:
        print("Carpetas encontradas:")
        for carpeta in carpetas:
            print(f"\n- {carpeta}")
            analizar_archivo(os.path.join(dpath, carpeta), carpeta)
    else:
        print("No se encontraron carpetas.")

def leer_csv(archivo_csv):
    """Lee un archivo CSV y maneja posibles errores."""
    try:
        df = pd.read_csv(archivo_csv, on_bad_lines='skip', quoting=3, delimiter=',')
        return df
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return None

def es_caracter_ileible(texto):
    """Determina si el texto contiene caracteres ilegibles."""
    return not re.match(r'^[\x00-\x7F]*$', texto)

def transformar_datos(df, field_names):
    """Transforma los datos del DataFrame en un formato más estructurado."""
    rows = []
    for doc_id in df['DocID'].unique():
        doc_data = df[df['DocID'] == doc_id]
        new_row = {field: None for field in field_names}
        new_row['DocID'] = doc_id
        for _, row in doc_data.iterrows():
            field_name = row['FieldName']
            field_value = row.get('FieldValue', None)
            if field_name == 'cmpunidp':
                continue
            if pd.notna(field_value) and es_caracter_ileible(str(field_value)):
                new_row[field_name] = 1
            else:
                new_row[field_name] = field_value
        rows.append(new_row)
    
    return pd.DataFrame(rows)

def preprocesed_versions(df):
    # Supongamos que tu DataFrame se llama df
    return df.sort_values(by='$REF', ascending=False)


def rename_duplicates(df, column):
    # Diccionario para contar cuántas veces aparece cada archivo (normalizado)
    file_count = {}
    
    # Iterar sobre cada ruta del archivo en la columna
    for i, file_path in enumerate(df[column]):
        # Verificar si el valor no es None o NaN
        if pd.isna(file_path):
            continue  # Saltar esta iteración si el valor es None o NaN
        
        # Obtener el directorio y el nombre de archivo con extensión
        directory, filename = os.path.split(file_path)
        file_base, file_ext = os.path.splitext(filename)

        # Normalizamos el nombre de archivo a minúsculas para evitar colisiones
        file_base_lower = file_base.lower()

        # Verificar si el archivo (en minúsculas) ya apareció antes
        if file_base_lower in file_count:
            # Si es repetido, incrementar el contador y renombrar
            file_count[file_base_lower] += 1
            new_file_name = f"{file_base}_{file_count[file_base_lower]}{file_ext}"
        else:
            # Si es la primera vez que aparece, inicializar el contador
            file_count[file_base_lower] = 0
            new_file_name = filename

        # Crear la nueva ruta con el nombre cambiado
        new_file_path = os.path.join(directory, new_file_name)

        # Verificar si el archivo original existe y es un archivo (no carpeta)
        if os.path.isfile(file_path):
            # Renombrar el archivo en el sistema de archivos
            os.rename(file_path, new_file_path)
            
            # Actualizar el DataFrame con la nueva ruta
            df.at[i, column] = new_file_path
        else:
            print(f"El archivo '{file_path}' no existe o no es un archivo.")

    return df

def analizar_archivo(dpath_carpeta, carpeta_nombre):
    archivo_csv = os.path.join(dpath_carpeta, "documents_info.csv")
    
    if not os.path.isfile(archivo_csv):
        print(f"No se encontró el archivo 'documents_info.csv' en {dpath_carpeta}.")
        return
    
    df = leer_csv(archivo_csv)
    if df is None or 'DocID' not in df.columns or 'FieldName' not in df.columns:
        print(f"El archivo 'documents_info.csv' no contiene las columnas esperadas en {dpath_carpeta}.")
        return

    # Obtener datos únicos
    doc_ids_unicos = df['DocID'].nunique()
    field_names = list(set(df['FieldName'].unique()))
    
    print(f"En la carpeta '{carpeta_nombre}':")
    print(f"Cantidad de DocID únicos: {doc_ids_unicos}")
    print(f"Cantidad de FieldName únicos: {len(field_names)}")
    
    # Transformar los datos
    transformed_data = transformar_datos(df, field_names)
    
    # Eliminar columna 'cmpunidp' si existe
    if 'cmpunidp' in transformed_data.columns:
        transformed_data = transformed_data.drop(columns=['cmpunidp'])
    
    # Reordenar columnas para que 'DocID' sea la primera
    columns_order = ['DocID'] + [col for col in transformed_data.columns if col != 'DocID']
    transformed_data = transformed_data[columns_order]
    
    # Limpiar y guardar
    # Reemplazar comillas vacías en cada celda
    transformed_data = transformed_data.apply(lambda col: col.str.replace('"', '') if col.dtype == 'object' else col)
    # Eliminar columnas vacías (sin datos)
    transformed_data = transformed_data.dropna(axis=1, how='all')
    # Renombrar  archivos  con igual nombre
    transformed_data = rename_duplicates(transformed_data,"cmpAnexoProc")

    # Guardar los datos transformados en un nuevo archivo CSV
    output_csv = os.path.join(dpath_carpeta, "transformed_data.csv")
    transformed_data.to_csv(output_csv, index=True)
    print(f"Datos transformados guardados en '{output_csv}'.")

# Ejemplo de uso
dpath = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"
listar_carpetas(dpath)
