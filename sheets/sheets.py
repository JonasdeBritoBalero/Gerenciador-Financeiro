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
# SAMPLE_RANGE_NAME = "!A1:C15"  espaço da planilha que sera verificada, intervalo de celulas

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



# atualiza os valores da carteira de todos os ativos
def atualizacao_ativos(valoresST):
  creds = autenticacao_google()
  ''' 1 - MXRF11
    2 - VRTA11
    3 - TGAR11
    4 - BBAS3
    5 - BBSE3
    6 - LEVE3
    7 - TAEE4
  '''
  ordem = ['MXRF11', 'VRTA11', 'TGAR11', 'BBAS3', 'BBSE3', 'LEVE3', 'TAEE4']

  valoresST = [valoresST[ativo] for ativo in ordem]
  # valores = [10.00]]
  valores = []
  for v in valoresST:
    valores.append([str(v).replace(".", ",")])
  # LEitura e escrita da planilha funciona  da seguinte forma:
  # planilha = [[coluna1, coluna2, coluna3], -> linha 1
  #            [coluna1, coluna2, coluna 3]] -> linha 2
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    SAMPLE_RANGE_NAME = "Renda_variavel!E21:E27"
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # adicionar/editar valores no Google Sheets
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME, valueInputOption="USER_ENTERED",
                                    body={"values": valores}).execute()
  except HttpError as err:
    print(err)

COLUNAS = {"MXRF11":"B", "VRTA11":"C", "TGAR11":"D", "BBAS3":"E", "BBSE3":"F", "LEVE3":"G", "TAEE4":"H"}
LINHAS = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# ativos = {"MXRF11": ['RENDIMENTO', "15/01/2025", 0.1]}
# Inserir os rendimentos que serão recebidos na tabela d, de forma individual
def Inserir_dividendos_sheets(ativo, data, valor):
  creds = autenticacao_google()
  try:
      service = build("sheets", "v4", credentials=creds)

      sheet = service.spreadsheets() # planilha
      # data = "2026-08-18"
      linha = LINHAS[int(data.split('-')[1])-1]
      coluna = COLUNAS[ativo]
      SAMPLE_RANGE_NAME2 = f"Renda_variavel!{coluna}{linha}"

      # procura se existe algum valor na celula
      result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME2).execute()
      values = result.get('values', [])
      # values = [ ["R$ 50,00"]]
      # se existir ele vai pegar e somar
      if values:
        # precisa fazer o tratamento do values para conseguir fazer a soma
        valor_final = valor + float(values[0][0].translate(str.maketrans({
        'R': '',
        '$': '',
        ',': '.'
        })))
      else:
        valor_final = valor
      valor_final = [[valor_final]] # valor para ser inserido na tabela
      # inseri o valor novo na tabela
      result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME2, valueInputOption="USER_ENTERED",
                                  body={"values": valor_final}).execute()



  except Exception as err:
      print(err)


# Passo 2: Definir qual planilha vai utilizar

# Passo 3: Definir o espaço na planilha que vai ser modificado

# Passo 4: Executar a ação de alteração ou inserção de dado.