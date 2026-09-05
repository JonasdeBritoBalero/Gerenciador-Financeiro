from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def pegar_ativo_completo(ativos):
    precos = {}
    dividendos = {}
    # Passo 1: Acessar o navegador e direciona para o site.
    navegador = webdriver.Chrome()
    
    navegador.maximize_window()
    navegador.get("https://investidor10.com.br/")
    for a in ativos:
        dividendo = []
        sucesso = False
        while not sucesso:
            try:
                # Passo 2: pesquisa do ativo
                pesquisa = navegador.find_element(By.XPATH, "//*[@id='search_button']/button")
                pesquisa.click()
                sleep(5)
                navegador.find_element(By.XPATH, "/html/body/div[4]/header/div[2]/div/div/form/div/span/input[2]").send_keys(a)
                sleep(2)
                navegador.find_element(By.XPATH, "//*[@id='btn-search-desktop']").click()
                sleep(5)
                navegador.find_element(By.XPATH, "//*[@id='searchPage']/section/div/div[3]/div/div[2]/div[2]/a").click()
                sleep(2)
                # Passo 3: Pega o valor do ativo
                preco = navegador.find_element(By.XPATH, "//*[@id='cards-ticker']/div[1]/div[2]/div/span[1]") # valor da ação/FIIS
                # Passo 4: Pega os dividendos do ativo
                n = 1
                while True:
                    divi1 = navegador.find_element(By.XPATH, f"//*[@id='table-dividends-history']/tbody/tr[{n}]")
                    divi1 = divi1.text.split()
                    data = divi1[2].split('/')
                    data_divi = datetime(int(data[2]), int(data[1]), int(data[0]))
                    if data_divi.date() > datetime.now().date():
                        dividendo.append(divi1) # Dividendo do FIIS/ações
                        n = n + 1
                    else:
                        break
                sleep(2)
                # Passo 5: registrar o valor atual do ativo
                precos[a] = float(preco.text.replace(",", ".").split()[1])
                # Passo 6: Se tiver dividendo ele será tratado e registrado
                if dividendo:
                    dividendos[a] = []
                    for d in dividendo:
                        del d[1]
                        d[1] = d[1].replace("/", "-") # mudar a data 15/01/2026 para 15-01-2025
                        d[1] = datetime.strptime(d[1], "%d-%m-%Y")
                        d[1] = d[1].strftime("%Y-%m-%d") # invertendo a data para o modelo padrão do banco de dados
                        d[2] = d[2].replace(",", ".")
                        d[2] = float(d[2])
                        dividendos[a].append(d)
                sucesso = True
                print("acesso a fiis ou acao")
            except Exception as e:
                navegador.get("https://investidor10.com.br/")
                print(f"Erro: {e}")
    
    return precos, dividendos