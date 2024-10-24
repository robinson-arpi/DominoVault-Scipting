import os
from AlfrescoClient import AlfrescoClient

def get_folders(path):
    items = os.listdir(path)
    return [item for item in items if os.path.isdir(os.path.join(path, item))]

def main():
    base_folder_path = r"C:\Users\robin\Desktop\Centrosur\RespaldoDomino"  # Cambia esto a tu directorio
    main_folder_name = "Test"  # Cambia el nombre si es necesario

    alfresco_client = AlfrescoClient()
    main_folder_id = alfresco_client.create_main_folder(main_folder_name)
    print("Nodo principal: " + main_folder_id)

    folders = get_folders(base_folder_path)

    for folder in folders:
        folder_id = alfresco_client.create_subfolder(main_folder_id, folder)

        folder_path = os.path.join(base_folder_path, folder)

        subfolders = get_folders(folder_path)
        print("a buscar  en: " + str(subfolders))
        for subfolder in subfolders:
            id_subfolder = alfresco_client.create_subfolder(folder_id,subfolder)
            csv_files = [file for file in os.listdir(os.path.join(folder_path, subfolder)) if file.endswith('.csv')]
            if "clean_data.csv" in csv_files:
                alfresco_client.process_csv_and_upload_attachments(os.path.join(folder_path, subfolder), "clean_data.csv", id_subfolder)
                


if __name__ == "__main__":
    main()
