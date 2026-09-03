from datetime import datetime
import sqlite3

# Passo 1: conexão com o banco
conexao = sqlite3.connect("Finanças.db")
cursor = conexao.cursor()
# Passo 2: Criação das tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Wallet (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ativo TEXT UNIQUE NOT NULL,
    TpAtivo TEXT,
    ValorTotal REAL,
    Quantidade INTEGER,
    PriceAvg REAL GENERATED ALWAYS AS (ROUND(ValorTotal/Quantidade, 2)) STORED
)
""")

# tabela compras/vendas
cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderBooks (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ativo TEXT NOT NULL,
    TpAtivo TEXT,
    Ordem TEXT CHECK(Ordem IN('C', 'V')), 
    Data TEXT, 
    Quantidade INTEGER,
    VlTotal REAL,
    FOREIGN KEY (Ativo) REFERENCES Wallet(Ativo)
)
""") 

# tabela da situação real do valor com o valor real
cursor.execute("""
CREATE TABLE IF NOT EXISTS CurrentValue (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ativo TEXT NOT NULL,
    TpAtivo TEXT,
    Data TEXT,
    VUAtual REAL,
    VTAtual REAL,
    Diferenca REAL,
    FOREIGN KEY (Ativo) REFERENCES Wallet(Ativo) 
)
""")
# VUAtual -> cotação atual de 1 ativo
# VTAtual -> valor do pratimonio atual (VUAtual * quanttidade da carteira)
# diferenca -> pega o valor total atual - valor total da carteira

#cursor.execute("DROP TABLE Proventos")
# tabela de proventos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Earnings (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Ativo TEXT NOT NULL,
    TpAtivo TEXT,
    TpEarnings TEXT,
    DataPag TEXT,
    ProUnitario REAL,
    proTotal REAL,
    FOREIGN KEY (Ativo) REFERENCES Wallet(Ativo)   
)
""")
# Passo 3: Criação do CRUD
# Create
# Criar ativo em ativo em wallet
def inserir_fundo(ativo, tpativo, valor, quant):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO Wallet (ativo, TpAtivo, ValorTotal, Quantidade) VALUES (?, ?, ?, ?)", (ativo, tpativo, valor, quant))
    
    conexao.commit()
    conexao.close()
# criar uma ordem de compra ou venda
def inserir_operacao(ativo, tpativo, ordem, quant, valor, data=None):
    
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    # data -> YYYY-MM-DD
    # Caso não seja preenchido a data é considerado a data que foi feito o apontamento
    if data is None:
        data = datetime.now().date()
    cursor.execute("INSERT INTO OrderBooks (Ativo, TpAtivo, Ordem, Data, Quantidade, VlTotal) VALUES (?, ?, ?, ?, ?)", (ativo, tpativo, ordem, data, quant, valor))
    # Quando comprar um ativo já e acrescentado na carteira
    if ordem == "C":
        cursor.execute("""
        UPDATE Wallet
        SET quantidade = quantidade + ?,
            valor_total = valor_total + ?
        where Ativo = ?
        """, (quant, valor, ativo))
    # Quando vender um ativo já é retirado da carteira
    elif ordem == "V":
        cursor.execute("""
        UPDATE Wallet
        SET quantidade = quantidade - ?,
            valor_total = valor_total - ?
        where Ativo = ?
        """, (quant, valor, ativo))
        
    conexao.commit()
    conexao.close()
# Valor atual do ativo
def inserir_atual(Ativo, TpAtivo, VUA, VTA, diferenca, data=None):
    
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    if data is None:
        data = datetime.now().date()
    cursor.execute("INSERT INTO CurrentValue (Ativo, TpAtivo, Data, VUAtual, VTAtual, diferenca) VALUES (?, ?, ?, ?, ?)", (Ativo,TpAtivo, data, VUA, VTA,diferenca))
    
    conexao.commit()
    conexao.close()
# Proventos dos ativos
def inserir_dividendo(ativo, tpativo, tpearn, data_p, valor_u, valor_t):
    # tabela -> FIIS ou Acoes
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    mes = data_p[0:8]+'%'
    cursor.execute(f"SELECT Ativo, TpEarnings, DataPag, ProUnitario FROM Earnings WHERE DataPag LIKE '{mes}' AND ativo = '{ativo}'")
    dadosativo = cursor.fetchall()
    print(dadosativo)
    adicionar = True
    for d in dadosativo:
        if d[1] == tpearn and d[3] == valor_u:
            print("Dividendo adcionado!")
            adicionar = False
            break
    
    if adicionar:
        cursor.execute(f"INSERT INTO Earnings (Ativo, TpAtivo, TpEarnings, DataPag, ProUnitario, ProTotal) VALUES (?, ?, ?, ?, ?, ?)", (ativo, tpativo, tpearn, data_p, valor_u, valor_t))
        # Atualização da planilha
        # atualizar_rendimento(ativo, data_p, valor_t)
        print("Adcionado com sucesso!")
    else:
        print("Já foi adicionado no banco de dados!")
    
    conexao.commit()
    conexao.close()
# Read
def read_wallet():
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT Ativo, TpAtivo, ValorTotal, Quantidade, PriceAVG FROM Wallet WHERE")
    dadosativos = cursor.fetchall()
    conexao.commit()
    conexao.close()

    return dadosativos

# Update -> Opcional incialmente
# Delete

# Passo 4: Fechar a conexão

conexao.commit()
conexao.close()