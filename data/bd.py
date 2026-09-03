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
    Valor_unidade_atual REAL,
    Valor_total_atual REAL,
    Diferenca REAL,
    FOREIGN KEY (Ativo) REFERENCES Wallet(Ativo) 
)
""")

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
# Read
# Update -> Opcional incialmente
# Delete

# Passo 4: Fechar a conexão

conexao.commit()
conexao.close()