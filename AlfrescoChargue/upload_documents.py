import requests
from requests.auth import HTTPBasicAuth
import json
import os
import pandas as pd
import  time
# Datos de conexión
alfresco_url = "http://172.19.154.129:8080/alfresco/api/-default-/public/alfresco/versions/1"
alfresco_user = "admin"
alfresco_password = "admin"

#Solución a error 504
# Definir el tiempo de espera y el número máximo de reintentos
REQUEST_TIMEOUT = 5  # Tiempo de espera en segundos
MAX_RETRIES = 3  # Número máximo de reintentos

# Función para realizar solicitudes con reintentos
def make_request(method, url, **kwargs):
    for attempt in range(MAX_RETRIES):
        try:
            response = method(url, **kwargs)
            response.raise_for_status()  # Lanzar un error para códigos de respuesta HTTP 4xx/5xx
            return response
        except requests.exceptions.HTTPError as e:
            #print(f"HTTP error: {e}")
            if response.status_code == 504:
                print("\033[93mError 504: Gateway Timeout. Retrying...\033[0m")
            elif response.status_code == 409:
                # Mensaje de error 409 en rojo
                print("\033[91m" + f"Error 409: Conflict. The request could not be processed due to a conflict with the current state of the target resource." + "\033[0m")
                print(f"Response Details: {response.text}")  # Imprime el texto de la respuesta
                break  # No reintentamos en caso de error 409
            else:
                break  # Si no es un 504, no reintentamos
        except requests.exceptions.RequestException as e:
            print("\033[91m" + f"Request exception: {e}" + "\033[0m")

            break  # Si hay otro tipo de error, salimos
        time.sleep(REQUEST_TIMEOUT)  # Esperar 2 segundos antes de reintentar
    return None

# Función para buscar si un nodo con el mismo nombre ya existe
def search_folder_by_name(folder_name):
    try:
        # URL para buscar el nombre de la carpeta usando la API de búsqueda
        url = f"{alfresco_url}/queries/nodes?term={folder_name}&nodeType=cm:folder"
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET para buscar la carpeta
        response = make_request(requests.get, url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers)
        
        if response is not None and response.status_code == 200:
            json_response = response.json()
            # Si se encuentra al menos un ítem, la carpeta ya existe
            if len(json_response['list']['entries']) > 0:
                node = json_response['list']['entries'][0]['entry']
                print(f"\033[94mThe folder '{folder_name}' already exists. ID: {node['id']}\033[0m")
                return node['id']  # Devolver el ID de la carpeta existente
        return None
    except Exception as e:
        print("\033[91m" + f"Error searching the folder: {e}" + "\033[0m")

        return None

# Función para crear una nueva carpeta
def create_main_folder(folder_name):
    try:
        parent_node_id = "-root-"
        
        # Verificar si la carpeta ya existe usando la API de búsqueda
        existing_folder_id = search_folder_by_name(folder_name)
        if existing_folder_id:
            return existing_folder_id  # Saltar creación y devolver el ID de la carpeta existente
        
        # URL para crear una nueva carpeta en el nodo raíz
        url = f"{alfresco_url}/nodes/{parent_node_id}/children"
        
        # Datos del nuevo nodo (la carpeta)
        data = {
            "name": folder_name,
            "nodeType": "cm:folder"  # Tipo de nodo, "cm:folder" es para carpetas
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud POST para crear la carpeta
        response = make_request(requests.post, url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers, data=json.dumps(data))
        
        # Verificar si la solicitud fue exitosa
        if response  is not None  and response.status_code == 201:
            node = response.json()["entry"]
            #print(f"Folder created: {node['name']} (ID: {node['id']})")
            return node['id']
        else:
            print(f"Error creating folder. Status code: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Función para crear subcarpetas
def create_subfolder(parent_id, subfolder_name):
    try:
        # Verificar si la subcarpeta ya existe en el nodo padre
        print("\nCreating subfolder:")
        search_url = f"{alfresco_url}/queries/nodes?term={subfolder_name}&nodeType=cm:folder"
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET para buscar la subcarpeta
        search_response = make_request(requests.get,search_url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers)
        
        if search_response is not None and search_response.status_code == 200:
            json_response = search_response.json()
            # Si se encuentra al menos un ítem, significa que la subcarpeta ya existe
            for entry in json_response['list']['entries']:
                node = entry['entry']
                if node['name'] == subfolder_name and node['parentId'] == parent_id:
                    print(f"The subfolder '{subfolder_name}' already exists. ID: {node['id']}")
                    return node['id']  # Devolver el ID de la carpeta existente
        
        # Si no existe, proceder a crearla
        create_url = f"{alfresco_url}/nodes/{parent_id}/children"
        
        # Datos del nuevo nodo (la subcarpeta)
        data = {
            "name": subfolder_name,
            "nodeType": "cm:folder"  # Tipo de nodo, "cm:folder" es para carpetas
        }
        
        # Realizar la solicitud POST para crear la subcarpeta
        create_response = make_request(requests.post, create_url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers, data=json.dumps(data))
        
        # Verificar si la solicitud fue exitosa
        if create_response is not None and create_response.status_code == 201:
            node = create_response.json()["entry"]
            #print(f"Subfolder created: {node['name']} (ID: {node['id']})")
            return node['id']
        else:
            print(f"Error creating subfolder. Status code: {create_response.status_code}")
            print("Response:", create_response.text)
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Filtrar solo las carpetas
def get_folders(path):
    items = os.listdir(path)
    return [item for item in items if os.path.isdir(os.path.join(path, item))]

# Función para verificar si el documento ya existe en la carpeta antes de subirlo
def document_exists(parent_id, document_name):
    try:
        search_url = f"{alfresco_url}/queries/nodes?term={document_name}&nodeType=cm:content"
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET para buscar el documento
        search_response = make_request(requests.get, search_url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers)
        
        if search_response is not None and search_response.status_code == 200:
            json_response = search_response.json()
            # Si se encuentra al menos un ítem, el documento ya existe
            for entry in json_response['list']['entries']:
                node = entry['entry']
                if node['name'] == document_name and node['parentId'] == parent_id:
                    print(f"\033[94mThe document '{document_name}' already exists. ID: {node['id']}\033[0m")
                    return node['id']  # Devolver el ID del documento
        return None  # Devolver None si el documento no existe
    except Exception as e:
        print(f"Error searching the document: {e}")
        return None  # Devolver None en caso de error


# Función para subir un archivo a Alfresco
def upload_document_to_alfresco(parent_id, file_path):
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        document_name = os.path.basename(file_path)
        
        # Verificar si el documento ya existe antes de intentar subirlo
        id_search = document_exists(parent_id, document_name)
        
        if id_search != None:
            #print(f"The document '{document_name}' already exists in node ID {parent_id}. It will not be uploaded again.")
            return id_search

        # URL para subir el documento al nodo padre
        url = f"{alfresco_url}/nodes/{parent_id}/children"
        
        # Datos para la creación del nodo del archivo
        files = {'filedata': open(file_path, 'rb')}
        data = {
            'name': document_name,  # Nombre del archivo en Alfresco
            'nodeType': 'cm:content'  # Tipo de nodo para archivos
        }
        
        response = make_request(requests.post, url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), files=files, data=data)
        
        if response is not None and response.status_code == 201:
            node = response.json()["entry"]
            print(f"Uploaded: {node['name']} (ID: {node['id']})")
            return node['id']  # Devolver el ID del documento subido
        else:
            print(f"Error uploading document. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error uploading document: {e}")
        return None

# Función para procesar el archivo CSV y subir adjuntos
def process_csv_and_upload_attachments(csv_path, csv_name,  parent_id_alfresco):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(os.path.join(csv_path, csv_name))

    # Recorrer cada fila del CSV
    for index, row in df.iterrows():
        # Obtener la ruta del archivo adjunto de la columna correspondiente
        file_path = row['cmpAnexoProc']

        # Subir el documento adjunto a Alfresco
        if pd.notna(file_path):  # Solo subir si hay una ruta
            #print(f"Uploading attachment: {file_path}")
            document_id = upload_document_to_alfresco(parent_id_alfresco, file_path)
            
            if document_id:
                #print(f"Attachment uploaded: {file_path} (ID: {document_id})\n")
                url_alfresco = f"{alfresco_url}/nodes/{document_id}?a=true"  # Enlace a Alfresco del documento
                df.at[index, 'cmpAnexoProc'] = url_alfresco
            else:
                print(f"Failed to upload: {file_path}\n")
    # Guardar el CSV actualizado en una ruta temporal
    csv_actualizado = 'enlaced_data_to_alfresco.csv'
    df.to_csv(os.path.join(csv_path, csv_actualizado), index=False)            

# Función principal para ejecutar todo
def main():
    # Definir ruta de la carpeta que contiene las subcarpetas
    base_folder_path = r"C:\Users\robin\Desktop\Centrosur\RespaldoDomino"  # Cambia esto a tu directorio
    
    # Nombre de la carpeta principal en Alfresco
    main_folder_name = "DominoVault"  # Cambia el nombre si es necesario

    # Crear la carpeta principal
    main_folder_id = create_main_folder(main_folder_name)
    
    # Recorrer todas las subcarpetas en la carpeta base
    folders = get_folders(base_folder_path)
    
    for folder in folders:
        # Crear cada subcarpeta en Alfresco
        folder_id = create_subfolder(main_folder_id, folder)
        
        # Ruta completa de la subcarpeta
        folder_path = os.path.join(base_folder_path, folder)
        
        subfolders = get_folders(folder_path)

        for subfolder in subfolders:
            id_subfolder = create_subfolder(folder_id, subfolder)

            # Procesar el archivo CSV en la subcarpeta
            csv_file_path = os.path.join(folder_path, subfolder)
            csv_name = "transformed_data.csv"
            if os.path.exists(csv_file_path):
                print(f"Processing CSV: {csv_file_path}")
                process_csv_and_upload_attachments(csv_file_path, csv_name,id_subfolder)
            else:
                print(f"No CSV file found in: {csv_file_path}")
    print("\033[92mEl proceso ha fallado con éxito :) \033[0m")

# Ejecutar la función principal
if __name__ == "__main__":
    main()