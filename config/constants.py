import configparser
import os

cfg = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'configurations.ini')

cfg.read(config_path, encoding="ansi")

# DATABASE
DRIVER = cfg["DATABASE"]["DRIVER"]
HOST = cfg["DATABASE"]["HOST"]
DATABASE = cfg["DATABASE"]["DATABASE"]
UID_DB = cfg["DATABASE"]["UID"]
PWD_DB = cfg["DATABASE"]["PWD"]

#ALFRESCO
ALFRESCO_URL = cfg['ALFRESCO']['URL']
ALFRESCO_USER = cfg['ALFRESCO']['USER']
ALFRESCO_PASSWORD = cfg['ALFRESCO']['PASSWORD']

# Acceder a la configuración de timeout y reintentos
REQUEST_TIMEOUT = int(cfg['ALFRESCO']['REQUEST_TIMEOUT'])
MAX_RETRIES = int(cfg['ALFRESCO']['MAX_RETRIES'])


# DIRECTORIES
PATH = cfg["DIRECTORIES"]["PATH"]