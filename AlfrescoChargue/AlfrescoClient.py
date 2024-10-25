import requests
from requests.auth import HTTPBasicAuth
import json
import time
import os
import pandas as pd
import sys

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.constants import ALFRESCO_URL, ALFRESCO_USER, ALFRESCO_PASSWORD, REQUEST_TIMEOUT, MAX_RETRIES

class AlfrescoClient:
    def __init__(self):
        # Inicializar el cliente de Alfresco con la URL base y autenticación
        self.base_url = ALFRESCO_URL
        self.auth = HTTPBasicAuth(ALFRESCO_USER, ALFRESCO_PASSWORD)

    def make_request(self, method, url, **kwargs):
        """
        Realiza una solicitud HTTP y maneja reintentos en caso de errores.
        
        Args:
            method: Método HTTP (get, post, etc.)
            url: URL a la que se realiza la solicitud
            **kwargs: Parámetros adicionales para la solicitud

        Returns:
            response: Objeto de respuesta si la solicitud es exitosa, None en caso de fallo.
        """
        for attempt in range(MAX_RETRIES):
            try:
                # Realiza la solicitud
                response = method(url, **kwargs)
                response.raise_for_status()  # Lanzar un error para códigos de respuesta HTTP 4xx/5xx
                return response
            except requests.exceptions.HTTPError as e:
                # Manejo de errores HTTP
                if response.status_code == 504:
                    print("\033[93mError 504: Gateway Timeout. Retrying...\033[0m")
                elif response.status_code == 409:
                    print("\033[91m" + f"Error 409: Conflict. The request could not be processed due to a conflict with the current state of the target resource." + "\033[0m")
                    print(f"Response Details: {response.text}")  # Imprime el texto de la respuesta
                    break  # No reintentamos en caso de error 409
                else:
                    break  # Si no es un 504, no reintentamos
            except requests.exceptions.RequestException as e:
                print("\033[91m" + f"Request exception: {e}" + "\033[0m")
                break  # Si hay otro tipo de error, salimos
            # Esperar antes de reintentar
            time.sleep(REQUEST_TIMEOUT)  
        return None

    def search_folder_by_name(self, folder_name):
        """
        Busca una carpeta en Alfresco por nombre.
        
        Args:
            folder_name: Nombre de la carpeta a buscar
        
        Returns:
            str: ID de la carpeta si existe, None si no.
        """
        try:
            # Construir la URL de búsqueda de carpeta
            url = f"{self.base_url}/queries/nodes?term={folder_name}&nodeType=cm:folder"
            headers = {"Content-Type": "application/json"}
            response = self.make_request(requests.get, url, auth=self.auth, headers=headers)

            # Comprobar si la respuesta es válida y contiene resultados
            if response is not None and response.status_code == 200:
                json_response = response.json()
                if len(json_response['list']['entries']) > 0:
                    node = json_response['list']['entries'][0]['entry']
                    print(f"\033[94mThe folder '{folder_name}' already exists. ID: {node['id']}\033[0m")
                    return node['id']  # Devolver el ID de la carpeta existente
            return None
        except Exception as e:
            print("\033[91m" + f"Error searching the folder: {e}" + "\033[0m")
            return None

    def create_main_folder(self, folder_name):
        """
        Crea una carpeta principal en Alfresco.
        
        Args:
            folder_name: Nombre de la carpeta a crear
        
        Returns:
            str: ID de la carpeta creada o existente, None en caso de error.
        """
        try:
            parent_node_id = "-root-"
            existing_folder_id = self.search_folder_by_name(folder_name)
            if existing_folder_id:
                return existing_folder_id  # Saltar creación y devolver el ID de la carpeta existente

            # Construir la URL para crear la carpeta
            url = f"{self.base_url}/nodes/{parent_node_id}/children"
            data = {
                "name": folder_name,
                "nodeType": "cm:folder"
            }
            headers = {"Content-Type": "application/json"}
            # Realizar la solicitud para crear la carpeta
            response = self.make_request(requests.post, url, auth=self.auth, headers=headers, data=json.dumps(data))

            # Comprobar si la creación fue exitosa
            if response is not None and response.status_code == 201:
                node = response.json()["entry"]
                return node['id']
            else:
                print(f"Error creating folder. Status code: {response.status_code}")
                print("Response:", response.text)
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def create_subfolder(self, parent_id, subfolder_name):
        """
        Crea una subcarpeta dentro de una carpeta existente en Alfresco.
        
        Args:
            parent_id: ID de la carpeta padre donde se creará la subcarpeta
            subfolder_name: Nombre de la subcarpeta a crear
        
        Returns:
            str: ID de la subcarpeta creada o existente, None en caso de error.
        """
        try:
            print(f"\nCreating subfolder: {subfolder_name}")
            # URL para buscar la subcarpeta existente
            search_url = f"{self.base_url}/queries/nodes?term={subfolder_name}&nodeType=cm:folder"
            headers = {"Content-Type": "application/json"}
            search_response = self.make_request(requests.get, search_url, auth=self.auth, headers=headers)

            # Comprobar si la subcarpeta ya existe
            if search_response is not None and search_response.status_code == 200:
                json_response = search_response.json()
                for entry in json_response['list']['entries']:
                    node = entry['entry']
                    if node['name'] == subfolder_name and node['parentId'] == parent_id:
                        print(f"The subfolder '{subfolder_name}' already exists. ID: {node['id']}")
                        return node['id']  # Devolver el ID de la subcarpeta existente

            # Si no existe, crear la subcarpeta
            create_url = f"{self.base_url}/nodes/{parent_id}/children"
            data = {
                "name": subfolder_name,
                "nodeType": "cm:folder"
            }
            create_response = self.make_request(requests.post, create_url, auth=self.auth, headers=headers, data=json.dumps(data))

            # Comprobar si la creación fue exitosa
            if create_response is not None and create_response.status_code == 201:
                node = create_response.json()["entry"]
                return node['id']
            else:
                print(f"Error creating subfolder {subfolder_name}. Status code: {create_response.status_code}")
                print("Response:", create_response.text)
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def document_exists(self, parent_id, document_name):
        """
        Verifica si un documento existe en Alfresco.
        
        Args:
            parent_id: ID de la carpeta padre donde se busca el documento
            document_name: Nombre del documento a verificar
        
        Returns:
            str: ID del documento si existe, None si no.
        """
        try:
            search_url = f"{self.base_url}/queries/nodes?term={document_name}&nodeType=cm:content"
            headers = {"Content-Type": "application/json"}
            search_response = self.make_request(requests.get, search_url, auth=self.auth, headers=headers)

            # Comprobar si la respuesta es válida y contiene resultados
            if search_response is not None and search_response.status_code == 200:
                json_response = search_response.json()
                for entry in json_response['list']['entries']:
                    node = entry['entry']
                    if node['name'] == document_name and node['parentId'] == parent_id:
                        print(f"\033[94mThe document '{document_name}' already exists. ID: {node['id']}\033[0m")
                        return node['id']  # Devolver el ID del documento
            return None
        except Exception as e:
            print(f"Error searching the document: {e}")
            return None  # Devolver None en caso de error

    def upload_document_to_alfresco(self, parent_id, file_path):
        """
        Sube un documento a Alfresco.
        
        Args:
            parent_id: ID de la carpeta padre donde se subirá el documento
            file_path: Ruta del archivo a subir
        
        Returns:
            str: ID del documento subido, None en caso de error.
        """
        try:
            # Comprobar si el archivo existe
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None

            document_name = os.path.basename(file_path)
            id_search = self.document_exists(parent_id, document_name)

            if id_search is not None:
                return id_search

            url = f"{self.base_url}/nodes/{parent_id}/children"
            files = {'filedata': open(file_path, 'rb')}
            data = {
                'name': document_name,
                'nodeType': 'cm:content'
            }
            response = self.make_request(requests.post, url, auth=self.auth, files=files, data=data)

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

    def process_csv_and_upload_attachments(self, csv_path, csv_name, parent_id_alfresco):
        df = pd.read_csv(os.path.join(csv_path, csv_name))

        for index, row in df.iterrows():
            file_path = row['cmpAnexoProc']

            if pd.notna(file_path):  # Solo subir si hay una ruta
                document_id = self.upload_document_to_alfresco(parent_id_alfresco, file_path)

                if document_id:
                    url_alfresco = f"{self.base_url}/nodes/{document_id}?a=true"
                    df.at[index, 'cmpAnexoProc'] = url_alfresco
                else:
                    print(f"Failed to upload: {file_path}\n")

        csv_actualizado = 'data_vinculed_to_alfresco.csv'
        df.to_csv(os.path.join(csv_path, csv_actualizado), index=False)