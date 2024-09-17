# Exportador de Documentos de Lotus Notes a CSV

Este proyecto contiene un agente en Java para Lotus Domino que permite exportar documentos de una base de datos Lotus Notes con formularios específicos, guardando tanto los datos de los campos como los archivos adjuntos en un formato legible y estructurado (CSV).

## Estructura del Código

El agente realiza las siguientes acciones:
1. Itera sobre una lista de nombres de formularios predefinidos.
2. Busca todos los documentos de la base de datos que usan esos formularios.
3. Exporta los datos de los campos de los documentos a archivos CSV.
4. Extrae y guarda cualquier archivo adjunto embebido dentro de los campos de tipo `RichText`.

### Funciones principales

- **exportDocuments(String formName, String exportDir)**:
   - Exporta documentos de un formulario dado a un archivo CSV.
   - Cada documento tiene una carpeta asignada dentro del directorio de exportación que almacena sus archivos adjuntos.
   - Se guarda el contenido de los campos en formato CSV con codificación UTF-8.
   
- **escapeCsv(String value)**:
   - Escapa caracteres especiales y elimina saltos de línea en los valores de los campos, garantizando que el formato CSV sea válido.

## Requisitos

Para ejecutar este agente, necesitarás:
- IBM Domino Server con soporte para Java.
- Acceso a una base de datos Lotus Notes.
- Configuración de un entorno de desarrollo compatible con agentes de Java en Lotus Notes.

## Estructura de los Archivos Exportados

El agente crea una carpeta por cada formulario. Dentro de estas carpetas:
- Se genera un archivo CSV llamado `documents_info.csv` con la siguiente estructura:
(Preferentemenete que exportDir lleve por nombre la base de datos para tener todo mejor estrcuturado)
exportDir/ 
├── frmRegistro/ 
│   ├── documents_info.csv 
│   ├── [DocumentID1]/ 
│   │   ├── attachment1.pdf 
│   │   └── attachment2.docx 
│   ├── [DocumentID2]/ 
│   │   ├── attachment1.jpg 
│   │   └── attachment2.xlsx 
│   └── ... 
└── frmProcedimiento/

## Configuración

### Directorio de Exportación

Asegúrate de modificar la ruta del directorio de exportación en el código:

String exportDir = "C:\\Users\\robin\\Desktop\\Centrosur\\RespaldoDomino\\ProPru";

Esta ruta debe existir en tu sistema o el agente intentará crearla automáticamente.

### Nombres de los Formularios

La lista de formularios a exportar se encuentra en esta parte del código:
String[] formNames = {"frmRegistro", "frmProcedimiento", "frmInformacion"};


### Modifica los nombres de los formularios de acuerdo a los formularios que desees exportar.

## Ejecución del Agente

Importa y ejecuta este agente en la consola de IBM Domino o Lotus Notes Designer.
El agente iterará sobre los formularios especificados y exportará los documentos a los directorios correspondientes.

### Manejo de Errores

El código incluye manejo de excepciones para capturar cualquier error durante el proceso de exportación. Se imprime un mensaje detallado en la consola en caso de problemas.

## Notas

Los campos de tipo RichText se procesan y los archivos adjuntos incrustados se extraen.
Los saltos de línea en los valores de los campos son eliminados y las comillas dobles son escapadas para mantener la integridad del archivo CSV.

## Contribuciones

Las mejoras y sugerencias son bienvenidas. No dudes en realizar un fork de este repositorio y enviar tus pull requests.