# Script para Procesamiento de Archivos CSV

Este script en Python está diseñado para procesar archivos CSV dentro de carpetas en un directorio específico. Realiza las siguientes tareas:

1. **Verificación del directorio**: Asegura que el directorio especificado existe y es válido.
2. **Listado de carpetas**: Muestra las carpetas dentro del directorio.
3. **Análisis de archivos CSV**:
   - Lee el archivo `documents_info.csv` en cada carpeta.
   - Filtra y transforma los datos:
     - Elimina la columna `cmpunidp` si está presente.
     - Reemplaza el contenido de las celdas con caracteres ilegibles por el valor `1`.
     - Elimina las columnas vacías.
     - Renombra archivos duplicados para evitar colisiones.
   - Guarda los datos transformados en un nuevo archivo CSV llamado `clean_data.csv`.

## Requisitos

- Python 3.x
- Instalar requirements.txt

## Uso

1. **Configurar el Directorio**: Cambia el valor de `path` en el script con la ruta al directorio que contiene las carpetas que deseas procesar:

   ```python
   path = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"

2. **Ejecutar el Script**: Ejecuta el script de Python en la terminal o desde un entorno de desarrollo:


   ```python
   clean_data.py
El script recorrerá todas las carpetas en el directorio especificado y procesará los archivos documents_info.csv dentro de cada una.


## Funcionamiento Detallado

### Funciones Principales

- **`check_directory(path)`**:
  - Verifica si el path existe y si es un directorio.
  - Imprime un mensaje de error si el directorio no existe o no es válido.

- **`review_directory(path)`**:
  - Lista todas las carpetas en el directorio dado.
  - Llama a analyze_file para procesar los archivos CSV dentro de cada carpeta.

- **`read_csv(archive)`**:
  - Lee un archivo CSV usando Pandas.
  - Maneja errores durante la lectura, como archivos corruptos o con formato incorrecto.

- **`is_unreadable_character(text)`**:
  - Determina si un texto contiene caracteres ilegibles usando una expresión regular.

- **`data_transform(df, field_names)`**:
  - Transforma los datos en el DataFrame:
  - Elimina la columna cmpunidp si está presente.
  - Reemplaza celdas con caracteres ilegibles por el valor 1.
  - Reordena las columnas para que DocID sea la primera.

- **`rename_duplicates(df, column)`**:
  - Renombra archivos con nombres duplicados dentro del DataFrame para evitar conflictos de nombres.

- **`analyze_file(path, carpeta_nombre)`**:
  - Analiza el archivo documents_info.csv en la carpeta dada:
  - Lee el archivo CSV.
  - Transforma los datos con data_transform.
  - Elimina columnas vacías.
  - Guarda los datos transformados en un archivo llamado clean_data.csv.

- **`delete_empty_folders(folder_path)`**:
  - Elimina carpetas vacías dentro de un directorio.

## Notas Adicionales
Asegúrate de que todas las carpetas en el directorio especificado contengan archivos documents_info.csv para que el script funcione correctamente.
El script asume que el archivo CSV contiene las columnas `DocID`, `FieldName`, y `FieldValue`.

Si tienes alguna pregunta o encuentras algún problema, no dudes en abrir un issue o contactarme  