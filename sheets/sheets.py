import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Instalação da biblioteca do google
# pip install python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Passo 1: Autenticar a maquina para acessar a planilha com um arquivo json.

# Passo 2: Definir qual planilha vai utilizar

# Passo 3: Definir o espaço na planilha que vai ser modificado

# Passo 4: Executar a ação de alteração ou inserção de dado.
