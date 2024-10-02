import requests
from requests.auth import HTTPBasicAuth
import os
import re

# Función para limpiar caracteres no válidos en nombres de archivo
def clean_filename(filename):
    # Reemplazar caracteres inválidos por guiones bajos o cualquier otro carácter que prefieras
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

# Función para descargar el archivo desde Alfresco
def download_file_from_alfresco(node_id, save_directory, username, password):
    base_url = f"http://172.19.154.72:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}/content"
    response = requests.get(base_url, auth=HTTPBasicAuth(username, password), stream=True)

    if response.status_code == 200:
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            if 'filename*=' in content_disposition:
                filename = content_disposition.split("filename*=")[-1].split("''")[-1].strip('"')
            elif 'filename=' in content_disposition:
                filename = content_disposition.split("filename=")[-1].strip('"')
            else:
                filename = f"archivo_descargado_{node_id}"

            # No limpiar caracteres, pero escapamos los que sean inválidos en nombres de archivo
            filename = clean_filename(filename)
        else:
            filename = f"archivo_descargado_{node_id}"

        save_path = os.path.join(save_directory, filename)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"Archivo descargado y guardado en: {save_path}")
    else:
        print(f"Error al descargar el archivo. Código de estado: {response.status_code}")

# Parámetros
node_id = "7044462f-90d1-48c2-8446-2f90d158c23e"
save_directory = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru/"
username = "admin"
password = "admin"

download_file_from_alfresco(node_id, save_directory, username, password)
