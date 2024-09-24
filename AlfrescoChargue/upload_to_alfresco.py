import os
import pandas as pd
import requests

# Configuración de Alfresco
alfresco_url = "http://172.19.154.120:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/-root-"
alfresco_username = "admin"
alfresco_password = "admin"

# Ruta base a la carpeta de respaldo
domino_base_path = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino"

# Función para autenticar en Alfresco
def get_headers():
    auth = requests.auth.HTTPBasicAuth(alfresco_username, alfresco_password)
    return {'Authorization': f'Basic {alfresco_username}:{alfresco_password}'}

# Función para crear una carpeta en Alfresco
def crear_carpeta(carpeta_padre_id, nombre_carpeta):
    url = f"{alfresco_url}{carpeta_padre_id}/children"
    headers = get_headers()
    data = {
        "name": nombre_carpeta,
        "nodeType": "cm:folder"
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        carpeta_id = response.json()['entry']['id']
        print(f"Carpeta '{nombre_carpeta}' creada exitosamente con ID: {carpeta_id}")
        return carpeta_id
    else:
        print(f"Error creando la carpeta {nombre_carpeta}: {response.text}")
        return None

# Función para subir un archivo a Alfresco
def subir_archivo_a_alfresco(carpeta_id, file_path, file_name):
    url = f"{alfresco_url}{carpeta_id}/children"
    headers = get_headers()
    
    files = {
        'filedata': (file_name, open(file_path, 'rb')),
    }
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 201:
        print(f"Archivo '{file_name}' subido exitosamente.")
    else:
        print(f"Error subiendo '{file_name}': {response.text}")

# Función para procesar cada carpeta y subir los archivos
def procesar_carpeta(base_path, alfresco_parent_id):
    for carpeta in os.listdir(base_path):
        carpeta_path = os.path.join(base_path, carpeta)
        
        if os.path.isdir(carpeta_path):
            # Crear carpeta en Alfresco
            carpeta_alfresco_id = crear_carpeta(alfresco_parent_id, carpeta)
            
            if carpeta_alfresco_id:
                # Iterar sobre los archivos dentro de la carpeta
                for archivo in os.listdir(carpeta_path):
                    archivo_path = os.path.join(carpeta_path, archivo)
                    
                    if archivo.endswith(".csv"):
                        print(f"Procesando archivo CSV: {archivo}")
                        # Leer CSV
                        df = pd.read_csv(archivo_path)
                        
                        # Subir archivo CSV a Alfresco
                        subir_archivo_a_alfresco(carpeta_alfresco_id, archivo_path, archivo)
                        
                        # Procesar los enlaces a documentos (columna 'cmpnotesurl')
                        for index, row in df.iterrows():
                            doc_url = row.get('cmpnotesurl')
                            if doc_url and doc_url.startswith("notes://"):
                                doc_local_path = "ruta/a/tu/documento/local/"  # Ajustar
                                doc_name = os.path.basename(doc_url)
                                
                                doc_path_local = os.path.join(doc_local_path, doc_name)
                                if os.path.exists(doc_path_local):
                                    subir_archivo_a_alfresco(carpeta_alfresco_id, doc_path_local, doc_name)
                                else:
                                    print(f"Documento local no encontrado: {doc_path_local}")

# Iniciar el procesamiento desde la carpeta 'Domino'
alfresco_root_id = "e250b9f4-232a-4786-90b9-f4232ab78686"  # Cambiar al ID de la carpeta raíz en Alfresco
procesar_carpeta(domino_base_path, alfresco_root_id)
