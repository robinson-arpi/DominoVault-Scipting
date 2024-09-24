import requests

# Configuración de Alfresco
alfresco_url = "http://172.19.154.120:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/"
alfresco_username = "admin"
alfresco_password = "admin"

# Función para autenticar en Alfresco
def get_headers():
    auth = requests.auth.HTTPBasicAuth(alfresco_username, alfresco_password)
    return {'Authorization': f'Basic {alfresco_username}:{alfresco_password}'}

# Función para verificar si un nodo existe
def verificar_nodo(nodo_id):
    url = f"{alfresco_url}{nodo_id}"
    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"El nodo con ID {nodo_id} existe.")
    elif response.status_code == 404:
        print(f"El nodo con ID {nodo_id} no se encontró.")
    else:
        print(f"Error al verificar el nodo: {response.text}")

# ID del nodo que deseas verificar
nodo_id = "e250b9f4-232a-4786-90b9-f4232ab78686"  # Cambia esto por el ID que quieres verificar

# Verificar el nodo
verificar_nodo(nodo_id)
