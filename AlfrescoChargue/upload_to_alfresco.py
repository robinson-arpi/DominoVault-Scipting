import os
from AlfrescoClient import AlfrescoClient
import sys

# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.constants import ALFRESCO_MAIN_DIRECTORIE, ALFRESCO_MAIN_NODE

def get_folders(path):
    items = os.listdir(path)
    return [item for item in items if os.path.isdir(os.path.join(path, item))]

def main():
    alfresco_client = AlfrescoClient()

    # Crear el nodo principal en caos de no existir
    main_folder_id = alfresco_client.create_main_folder(ALFRESCO_MAIN_NODE)
    print("Nodo principal: " + main_folder_id)

    # Obtención de carpetas dentro del directorio donde se realiza el respaldo
    folders = get_folders(ALFRESCO_MAIN_DIRECTORIE)

    # Iteración sobre cada carpeta (NSF)
    for folder in folders:

        #Creación de subcarpeta(NSF) en  alfresco (devuelve el id si ya existe)
        folder_id = alfresco_client.create_subfolder(main_folder_id, folder)

        # Path para obtención de  carpetas correspondientes a los formularios de domino
        folder_path = os.path.join(ALFRESCO_MAIN_DIRECTORIE, folder)

        # Obtención de carpetas
        subfolders = get_folders(folder_path)

        #ITeracion correspondiente a  los forms dentro de  cada carpeta que corresponde  a una nsf
        for subfolder in subfolders:
            # Creación de subcarpeta (Form) en alfresco (devuelve el id si ya existe)
            id_subfolder = alfresco_client.create_subfolder(folder_id,subfolder)
            
            # Busqueda de archvios csv generados en procesos anteriores
            csv_files = [file for file in os.listdir(os.path.join(folder_path, subfolder)) if file.endswith('.csv')]

            # Si se genero el csv con datos limpios, se emplea para saber que documentos subir 
            # Se genera un csv llamado dato_vonculed_to_alfresco.csv para su carga psterior a db2
            if "clean_data.csv" in csv_files:
                alfresco_client.process_csv_and_upload_attachments(os.path.join(folder_path, subfolder), "clean_data.csv", id_subfolder)
                


if __name__ == "__main__":
    main()
