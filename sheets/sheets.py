import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Instalação da biblioteca do google
# https://developers.google.com/workspace/sheets/api/quickstart/python?hl=pt-br
# pip install python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Arquivos:
# Client_Secret.json -> As informações do usário para acessar a API, que você baixa da própria API pela primeira vez
# Token.json -> Manter as autenticação continua sem precisar toda vez fazer autenticação no google


# Passo 1: Autenticar a maquina para acessar a planilha com um arquivo json.

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] # tipo de atorização o seu codigo vai ter, nesse caso vai pode editar a planilha do jeito que desejar

load_dotenv()

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID") # id da planilha
SAMPLE_RANGE_NAME = "!A1:C15" # espaço da planilha que sera verificada, intervalo de celulas

def autenticacao_google():
  creds = None
  # autenticando o nosso código e conectando com a API do google
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    # Verifica se as credenciais expiraram e atualiza sozinho
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else: # caso seja a primeira vez realizando esse processo
      # utiliza o arquivo das suas informações do da api google
      flow = InstalledAppFlow.from_client_secrets_file(
          "Client_Secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  return creds


def manipulacao_sheet():
  creds = autenticacao_google()
  # LEitura e escrita da planilha funciona  da seguinte forma:
  # planilha = [[coluna1, coluna2, coluna3], -> linha 1
  #            [coluna1, coluna2, coluna 3]] -> linha 2
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    print("Name, Major:")
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      print(f"{row}")
    # Adicionar valores no google sheet
    valores_adicionar = [[""],
                         [""],
                         [""]]
    # valueInputOptions="USER_ENTERED" -> você pode colocar valores ou formulas na celula
    result = (
            sheet.values()
            .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="2026:C39", valueInputOption="USER_ENTERED", body={"values": valores_adicionar})
            .execute()
        )
  except HttpError as err:
    print(err)

if __name__ == "__main__":
  manipulacao_sheet()

# Passo 2: Definir qual planilha vai utilizar

# Passo 3: Definir o espaço na planilha que vai ser modificado

# Passo 4: Executar a ação de alteração ou inserção de dado.