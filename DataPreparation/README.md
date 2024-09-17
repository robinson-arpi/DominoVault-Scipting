# Script de Procesamiento de Archivos CSV

Este script en Python está diseñado para procesar archivos CSV dentro de carpetas en un directorio específico. Realiza las siguientes tareas:

1. **Verifica la existencia y validez del directorio**.
2. **Lista las carpetas en el directorio especificado**.
3. **Analiza los archivos CSV dentro de cada carpeta**:
   - Lee el archivo `documents_info.csv`.
   - Filtra y transforma los datos:
     - Elimina columnas que contengan el nombre `cmpunidp`.
     - Reemplaza el contenido de las celdas con caracteres ilegibles por el valor `1`.
     - Elimina columnas vacías.
   - Guarda los datos transformados en un nuevo archivo CSV llamado `transformed_data.csv`.

## Requisitos

- Python 3.x
- Pandas (puede instalarse usando `pip install pandas`)

## Uso

1. **Configurar el Directorio**: Establece el valor de `dpath` con la ruta al directorio que contiene las carpetas a procesar.

   ```python
   dpath = "C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru"

2. **Ejecutar el Script**: Ejecuta el script de Python. El script recorrerá todas las carpetas en el directorio especificado y procesará los archivos documents_info.csv dentro de cada una.

python tranformatio_data.py


## Funcionamiento Detallado

### Funciones Principales

- **`verificar_directorio(path)`**:
  - Verifica si el `path` existe y si es un directorio.
  - Imprime un mensaje de error si el directorio no existe o no es válido.

- **`listar_carpetas(dpath)`**:
  - Lista todas las carpetas en el directorio dado.
  - Llama a `analizar_archivo` para cada carpeta encontrada.

- **`leer_csv(archivo_csv)`**:
  - Lee un archivo CSV usando Pandas.
  - Maneja posibles errores al leer el archivo.

- **`es_caracter_ileible(texto)`**:
  - Determina si el texto contiene caracteres ilegibles usando una expresión regular.

- **`transformar_datos(df, field_names)`**:
  - Transforma los datos en el DataFrame:
    - Elimina columnas con el nombre `cmpunidp`.
    - Reemplaza el contenido de celdas con caracteres ilegibles por `1` (como en el caso de las columnas Check para el Scanned).
    - Reordena las columnas para que `DocID` sea la primera.

- **`analizar_archivo(dpath_carpeta, carpeta_nombre)`**:
  - Analiza el archivo `documents_info.csv` en la carpeta dada:
    - Lee el archivo CSV.
    - Transforma los datos usando `transformar_datos`.
    - Elimina columnas vacías.
    - Guarda los datos transformados en un nuevo archivo CSV llamado `transformed_data.csv`.


## Notas Adicionales
Asegúrate de que todas las carpetas en el directorio especificado contengan archivos documents_info.csv para que el script funcione correctamente.
El script asume que el archivo CSV contiene las columnas DocID, FieldName, y FieldValue.

Si tienes alguna pregunta o encuentras algún problema, no dudes en abrir un issue o contactarme