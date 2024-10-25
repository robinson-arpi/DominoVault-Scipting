## Proyecto de scripting para extracción de datos de lotus domino

Los scripts estpan diseñados para extraer información de lotus domino y subirla a alfresco en caso de archivos adjuntos y a db2 para la información correspondiente a cada archivo.

## Desarrollo

* VSCode
* Python 3.12.3

### Ejecución

> Clone el repositorio
>
> ```
>  git clone https://github.com/robinson-arpi/DominoVault-Scripting.git
> ```

Situese en la carpeta del proyecto e instale el requirements.txt

> Instale requirements.txt
>
> ```python
> pip install -r requirements.txt
> ```

#### Configuración de credenciales

> En config/configurations.ini agregar las  credenciales correspondientes para las conexiones  y directorios:
>
> ```
> #Credenciales para constants.py
>
> # Credenciales para DB2
> [DATABASE]
> DRIVER = {iSeries Access ODBC Driver}
> HOST = XXX.XXXX.XXX.XXX
> DATABASE = db_name
> UID = db_user
> PWD = db_pass
>
>
> #Credenciales para Alfresco
> [ALFRESCO]
> URL = api_url
> USER = af_user
> PASSWORD = af_admin
> # Tiempo de espera en segundos
> REQUEST_TIMEOUT = 5
> # Número máximo de reintentos
> MAX_RETRIES = 3
>
>
> [DIRECTORIES]
> MAIN_NODE = name_node
> MAIN_DIRECTORIE = path_directorie
>
> #Cambiar path para cada base de datos
> PATH_FOR_NSF = C:/Users/robin/Desktop/Centrosur/RespaldoDomino/ProPru
>
> ```

## Scripts

Existen 4 scripts, que deben ser ejecutados secuencialemente, a continuación se nombre el orden y dentro de cada uno de estos existe un readme explicando detalladamente su funcionamiento, entradas y salidas.

### 1. JavaAgent

Contiene un agente Java de Lotus Domino 9 para exportar todos los elementos de un form dentro de una base de datos.

### 2. DataPreparation

Script de python que toma lo extraído con el Agente Java para limpiar y organizar los datos.

### 3. AlfrescoMapping

Script de python que con la data limpia carga al gestor documental Alfresco los archivos adjutnos y vincula el nodo a un nuevo csv llamado data_vincules_to_alfresco.csv.

### 4. Db2_mapping

Script de python para subir como tabla el csv a base de datos, con el vinculo correspondiente a alfresco (Incompleto, solo realiza conexión a db2).

### Notas

* La carpeta Resources contiene solo imágenes que fueron usadas para crear los diferentes READMEs.
* En caso de necesitar credenciales extra se puedne agregar en configurations.ini y en constants.py

## Glosario de términos de lotus domino

* **Documento** : La unidad básica de almacenamiento de datos en Lotus Domino, similar a un registro en una base de datos. Cada documento puede contener varios campos con diferentes tipos de datos.
* **Formulario** : Una plantilla utilizada para crear documentos en una base de datos. Los formularios definen la estructura y el diseño de los documentos, así como los campos que se pueden completar.
* **Vista** : Una representación estructurada de los documentos en una base de datos. Las vistas permiten a los usuarios ver y filtrar documentos según criterios específicos, y pueden presentar datos en un formato tabular.
* **Base de Datos**: Un contenedor que almacena documentos, vistas, formularios y otros objetos. Las bases de datos en Lotus Domino tienen la extensión `.nsf`.
* **Agente** : Un script o programa que se ejecuta en el servidor de Domino para realizar tareas automatizadas, como la manipulación de documentos, la generación de informes o el envío de correos electrónicos.

## Contribuciones

¡Gracias por usar este proyecto! Si tienes algún problema o sugerencia, no dudes en abrir un issue o contribuir al proyecto.

<div align="center">
  <h3>Gerardo Arpi</h3>
  <p>Computer Science Engineer | Full Stack Developer | Data Analyst</p>
  <h3>Contact Me</h3>
  <a href="https://www.linkedin.com/in/robinson-arpi">
    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://wa.me/593998320642" target="_blank">
    <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp" />
  </a>
  <a href="mailto:robinson.arpi@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="GMail" />
  </a>
</div>
