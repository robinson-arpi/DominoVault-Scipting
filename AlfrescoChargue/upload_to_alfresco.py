import requests
import pandas as pd
import os

# Datos de configuración de Alfresco
ALFRESCO_URL = "http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1"
ALFRESCO_USERNAME = "admin"
ALFRESCO_PASSWORD = "admin"
PARENT_FOLDER_ID = "ProPru"  # ID del nodo donde se van a crear las carpetas

# Función para autenticación
def alfresco_auth():
    session = requests.Session()
    session.auth = (ALFRESCO_USERNAME, ALFRESCO_PASSWORD)
    return session

# Función para crear una carpeta en Alfresco
def create_folder(session, folder_name, parent_id):
    url = f"{ALFRESCO_URL}/nodes/{parent_id}/children"
    payload = {
        "name": folder_name,
        "nodeType": "cm:folder"
    }
    response = session.post(url, json=payload)
    if response.status_code == 201:
        print(f"Carpeta '{folder_name}' creada exitosamente.")
        return response.json()['entry']['id']  # ID de la nueva carpeta
    else:
        print(f"Error al crear la carpeta '{folder_name}': {response.text}")
        return None

# Función para subir un documento a una carpeta en Alfresco
def upload_document(session, folder_id, file_path):
    url = f"{ALFRESCO_URL}/nodes/{folder_id}/children"
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as file_data:
        files = {
            'filedata': (file_name, file_data)
        }
        response = session.post(url, files=files)
        
        if response.status_code == 201:
            print(f"Documento '{file_name}' subido correctamente.")
        else:
            print(f"Error al subir el documento '{file_name}': {response.text}")

# Leer el archivo CSV
def process_csv_and_upload(csv_path):
    # Leer el CSV con pandas
    data = pd.read_csv(csv_path)
    
    # Autenticación en Alfresco
    session = alfresco_auth()
    
    # Procesar cada fila del CSV
    for index, row in data.iterrows():
        folder_name = row['ID_Carpeta']  # Nombre de la carpeta a crear
        document_path = row['Ruta_Documento']  # Ruta del documento adjunto
        
        # Crear la carpeta en Alfresco
        folder_id = create_folder(session, folder_name, PARENT_FOLDER_ID)
        
        # Si la carpeta fue creada exitosamente, subimos el documento
        if folder_id:
            upload_document(session, folder_id, document_path)

# Ejecutar el proceso
if __name__ == "__main__":
    # Ruta del CSV a procesar
    csv_file_path = "ruta/a/tu/archivo.csv"
    process_csv_and_upload(csv_file_path)
