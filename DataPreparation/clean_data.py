import os
import shutil
import pandas as pd
import re

def check_directory(path):
    """Verifica si el path existe y es un directorio."""
    try:
        # Verifica si el path existe
        if not os.path.exists(path):
            print("\033[91mEl directorio '{}' no existe.\033[0m".format(path))
            return False
        # Verifica si el path es un directorio
        if not os.path.isdir(path):
            print("\033[91m'{}' no es un directorio.\033[0m".format(path))
            return False
        return True
    except Exception as e:
        # Captura e imprime cualquier error inesperado en rojo
        print("\033[91mError: {}\033[0m".format(e))
        return False

def review_directory(path):
    """Lista las carpetas en un directorio dado y analiza los archivos dentro de ellas."""
    # Verifica si el directorio es válido
    if not check_directory(path):
        return
    
    # Obtiene una lista de nombres de carpetas en el directorio
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    
    # Si se encontraron carpetas que corresponden a las bases de datos
    if folders:
        print("Carpetas encontradas:")
        for folder in folders:
            # Imprime el nombre de la carpeta
            print(f"\n- {folder}")
            # Llama a la función para analizar archivos dentro de la carpeta
            analyze_file(os.path.join(path, folder), folder)
    else:
        # Si no se encontraron carpetas, imprime un mensaje de error en rojo
        print("\033[91mError: No se encontraron carpetas.\033[0m")

def read_csv(archive):
    """Lee un archivo CSV y maneja posibles errores."""
    try:
        df = pd.read_csv(archive, on_bad_lines='skip', quoting=3, delimiter=',')
        return df
    except Exception as e:
        print(f"\033[91mError al leer el archivo: {e}.\033[0m")
        return None

def is_unreadable_character(text):
    """Determina si el texto contiene caracteres ilegibles."""
    return not re.match(r'^[\x00-\x7F]*$', text)

def data_transform(df, field_names):
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
            # Los caracteres ilegibles  corresponden a  casillas de verificación, para no perder la información, si existe algún caracter de estos el campo es reemplazado por 1
            if pd.notna(field_value) and is_unreadable_character(str(field_value)):
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
            print(new_file_name)
        else:
            # Si es la primera vez que aparece, inicializar el contador
            file_count[file_base_lower] = 0
            new_file_name = filename

        # Crear la nueva ruta con el nombre cambiado
        new_file_path = os.path.join(directory, new_file_name)

        # Verificar si el archivo original existe y es un archivo (no carpeta)
        if os.path.isfile(file_path):
            if os.path.exists(new_file_path):
                # Actualizar el DataFrame con la nueva ruta
                df.at[i, column] = new_file_path
                continue
            else:
                # Crear archivo nueov con el nomrb eactualziado
                shutil.copy(file_path, new_file_path)
        else:
            print(f"\033[91mEl archivo no existe: {file_path}.\033[0m")
    return df

def delete_empty_folders(folder_path):
    # Recorre las carpetas desde el nivel más profundo
    for current_folder, subfolders, files in os.walk(folder_path, topdown=False):
        # Si la carpeta está vacía (no contiene archivos ni subcarpetas)
        if not subfolders and not files:
            try:
                os.rmdir(current_folder)  # Elimina la carpeta vacía
            except OSError as e:
                # Imprime en rojo si ocurre un error al eliminar la carpeta
                print("\033[91mNo se pudo eliminar la carpeta {}: {}\033[0m".format(current_folder, e))
    # Imprime en verde si la carpeta se eliminó correctamente
    print("\033[92mCarpetas vacías eliminadas correctamente: {}\033[0m".format(current_folder))

def analyze_file(path, carpeta_nombre):
    delete_empty_folders(path)

    csv_archive = os.path.join(path, "documents_info.csv")
    if not os.path.isfile(csv_archive):
        print(f"\033[93mNo se encontró el archivo 'documents_info.csv' en {path}.\033[0m")
        return
    
    df = read_csv(csv_archive)
    if df is None or 'DocID' not in df.columns or 'FieldName' not in df.columns:
        print(f"\033[93mEl archivo 'documents_info.csv' no contiene las columnas esperadas en {path}.\033[0m")
        return

    # Obtener datos únicos
    unique_id_docs = df['DocID'].nunique()
    field_names = list(set(df['FieldName'].unique()))
    
    print(f"En la carpeta '{carpeta_nombre}':")
    print(f"Cantidad de DocID únicos: {unique_id_docs}")
    print(f"Cantidad de FieldName únicos: {len(field_names)}")
    
    # Transformar los datos
    transformed_data = data_transform(df, field_names)
    
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
    output_csv = os.path.join(path, "clean_data.csv")
    transformed_data.to_csv(output_csv)
    print(f"\033[92mDatos transformados guardados en '{output_csv}'.\033[0m")

# Ejemplo de uso
path = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"
review_directory(path)
