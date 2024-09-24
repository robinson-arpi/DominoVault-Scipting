import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Datos de conexión
alfresco_url = "http://172.19.154.120:8080/alfresco/api/-default-/public/alfresco/versions/1"
alfresco_user = "admin"
alfresco_password = "admin"

# Función para buscar si un nodo con el mismo nombre ya existe
def buscar_carpeta_por_nombre(nombre_carpeta):
    try:
        # URL para buscar el nombre de la carpeta usando la API de búsqueda
        url = f"{alfresco_url}/queries/nodes?term={nombre_carpeta}&nodeType=cm:folder"
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET para buscar la carpeta
        response = requests.get(url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers)
        
        if response.status_code == 200:
            respuesta_json = response.json()
            # Si se encuentra al menos un ítem, la carpeta ya existe
            if len(respuesta_json['list']['entries']) > 0:
                nodo = respuesta_json['list']['entries'][0]['entry']
                print(f"La carpeta '{nombre_carpeta}' ya existe. ID: {nodo['id']}")
                return nodo['id']  # Devolver el ID de la carpeta existente
        return None
    except Exception as e:
        print(f"Error al buscar la carpeta: {e}")
        return None

# Función para crear una nueva carpeta
def crear_carpeta_principal(nombre_carpeta):
    try:
        parent_node_id = "-root-"
        
        # Verificar si la carpeta ya existe usando la API de búsqueda
        id_carpeta_existente = buscar_carpeta_por_nombre(nombre_carpeta)
        if id_carpeta_existente:
            return id_carpeta_existente  # Saltar creación y devolver el ID de la carpeta existente
        
        # URL para crear una nueva carpeta en el nodo raíz
        url = f"{alfresco_url}/nodes/{parent_node_id}/children"
        
        # Datos del nuevo nodo (la carpeta)
        data = {
            "name": nombre_carpeta,
            "nodeType": "cm:folder"  # Tipo de nodo, "cm:folder" es para carpetas
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud POST para crear la carpeta
        response = requests.post(url, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers, data=json.dumps(data))
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 201:
            nodo = response.json()["entry"]
            print(f"Carpeta creada: {nodo['name']} (ID: {nodo['id']})")
            return nodo['id']
        else:
            print(f"Error al crear carpeta. Código de estado: {response.status_code}")
            print("Respuesta:", response.text)
            return None
    except Exception as e:
        print(f"Error durante la conexión: {e}")
        return None

# Función para crear subcarpetas
def subfolder_alfresco_creation(id_padre, nombre_subcarpeta):
    try:
        # Verificar si la subcarpeta ya existe en el nodo padre
        print("\nCreaicon carpeta:")
        url_busqueda = f"{alfresco_url}/queries/nodes?term={nombre_subcarpeta}&nodeType=cm:folder"
        headers = {
            "Content-Type": "application/json"
        }

        # Realizar la solicitud GET para buscar la subcarpeta
        response_busqueda = requests.get(url_busqueda, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers)
        
        if response_busqueda.status_code == 200:
            respuesta_json = response_busqueda.json()
            # Si se encuentra al menos un ítem, significa que la subcarpeta ya existe
            for entry in respuesta_json['list']['entries']:
                nodo = entry['entry']
                if nodo['name'] == nombre_subcarpeta and nodo['parentId'] == id_padre:
                    print(f"La subcarpeta '{nombre_subcarpeta}' ya existe. ID: {nodo['id']}")
                    return nodo['id']  # Devolver el ID de la carpeta existente
        
        # Si no existe, proceder a crearla
        url_creacion = f"{alfresco_url}/nodes/{id_padre}/children"
        
        # Datos del nuevo nodo (la subcarpeta)
        data = {
            "name": nombre_subcarpeta,
            "nodeType": "cm:folder"  # Tipo de nodo, "cm:folder" es para carpetas
        }
        
        # Realizar la solicitud POST para crear la subcarpeta
        response_creacion = requests.post(url_creacion, auth=HTTPBasicAuth(alfresco_user, alfresco_password), headers=headers, data=json.dumps(data))
        
        # Verificar si la solicitud fue exitosa
        if response_creacion.status_code == 201:
            nodo = response_creacion.json()["entry"]
            print(f"Subcarpeta creada: {nodo['name']} (ID: {nodo['id']})")
            return nodo['id']
        else:
            print(f"Error al crear subcarpeta. Código de estado: {response_creacion.status_code}")
            print("Respuesta:", response_creacion.text)
            return None
    except Exception as e:
        print(f"Error durante la conexión: {e}")
        return None

# Filtrar solo las carpetas
def get_folders(path):
    items = os.listdir(path)
    return [item for item in items if os.path.isdir(os.path.join(path, item))]

# Función para continuar con las siguientes acciones
def folder_creation(id_nodo, path):
    print(f"\n----------------\nCreando subcarpetas: {id_nodo}")
    # Filtrar solo las carpetas
    folders = get_folders(path)
    for folder in folders:
        # Crear la subcarpeta en Alfresco y obtener su ID
        id_subfolder = subfolder_alfresco_creation(id_nodo, folder)
        
        if id_subfolder:  # Si la subcarpeta fue creada o ya existía
            # Obtener las subcarpetas del siguiente nivel (solo un nivel más)
            subfolders_path = os.path.join(path, folder)
            subfolders = get_folders(subfolders_path)
            
            # Crear solo las subcarpetas del siguiente nivel
            for subfolder in subfolders:
                id_subsub = subfolder_alfresco_creation(id_subfolder, subfolder)
                print("--->" + id_subsub)

# Llama a la función para crear el nodo principal
nombre_nodo_principal = "DominoVault"
id_nodo_principal = crear_carpeta_principal(nombre_nodo_principal)
print(f"ID del nodo principal: {id_nodo_principal}")

# Continuar con las siguientes acciones si el nodo principal fue creado o ya existía
path = r"C:\Users\robin\Desktop\Centrosur\RespaldoDomino"

if id_nodo_principal:
    folder_creation(id_nodo_principal, path)