from datetime import datetime
from WebScraping.scraper import verificar_tp_ativo
from sheets.sheets import Inserir_dividendos_sheets
import sqlite3

# Criação do CRUD
# C -> Create
# Criar ativo em ativo em wallet
def inserir_ativo(ativo, tpativo, valor, quant):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO Wallet (ativo, TpAtivo, ValorTotal, Quantidade) VALUES (?, ?, ?, ?)", (ativo, tpativo, valor, quant))
    
    conexao.commit()
    conexao.close()
# criar uma ordem de compra ou venda
def inserir_ordem(ativo, ordem, quant, valor, data=None):
    print(data, " - crud")
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    # data -> YYYY-MM-DD
    # Caso não seja preenchido a data é considerado a data que foi feito o apontamento
    if data is None:
        data = datetime.now().date()
    cursor.execute("INSERT INTO OrderBooks (Ativo, Ordem, Data, Quantidade, VlTotal) VALUES (?, ?, ?, ?, ?)", (ativo, ordem, data, quant, valor))
    # Quando comprar um ativo já e acrescentado na carteira
    if ordem == "C":
        # Verificar se o ativo existe na carteira
        ativos = read_nome_ativos()
        existe = ativo in ativos
        # se existir
        if existe:
            cursor.execute("""
            UPDATE Wallet
            SET quantidade = quantidade + ?,
                valor_total = valor_total + ?
            where Ativo = ?
            """, (quant, valor, ativo))
            conexao.commit()
            conexao.close()
        # se não existir
        else:
            conexao.commit()
            conexao.close()
            tpativo = verificar_tp_ativo(ativo)
            inserir_ativo(ativo, tpativo, valor, quant)
            
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
def inserir_atual(Ativo, VUA, VTA, diferenca, data=None):
    
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    
    if data is None:
        #data = datetime.now().date()
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO CurrentValue (Ativo, Data, VUAtual, VTAtual, diferenca) VALUES (?, ?, ?, ?, ?)", (Ativo, data, VUA, VTA,diferenca))
    
    conexao.commit()
    conexao.close()
# InserirProventos dos ativos
def inserir_dividendo(ativo, tpearn, data_p, valor_u, valor_t):
    # tabela -> FIIS ou Acoes
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    # verificar se o dividendo ja foi adicionado no BD
    adicionar = verificando_dividendo(cursor, ativo, tpearn, data_p, valor_u)
    
    if adicionar:
        # inseri o dividendo no banco de dados
        cursor.execute(f"INSERT INTO Earnings (Ativo, TpEarnings, DataPag, ProUnitario, ProTotal) VALUES (?, ?, ?, ?, ?)", (ativo, tpearn, data_p, valor_u, valor_t))
        # Atualização da planilha
        Inserir_dividendos_sheets(ativo, data_p, valor_t)
        print("Adicionando na banco de dados!")
    else:
        print("Já existe no banco de dados")
    
    conexao.commit()
    conexao.close()

# R -> Read
def read_table(table):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    dados = cursor.fetchall()
    conexao.commit()
    conexao.close()

    return dados

# retorna somente os nomes dos ativos em carteira em uma lista
def read_nome_ativos():
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT ativo FROM Wallet")
    dados = cursor.fetchall()
    conexao.commit()
    conexao.close()
    ativos = [linha[0] for linha in dados]
    return ativos

def verificando_dividendo(cursor, ativo, tpearn, data, valor_u):
    mes = data[0:8]+'%'
    cursor.execute("SELECT Ativo, TpEarnings, DataPag, ProUnitario FROM Earnings WHERE DataPag LIKE ? AND ativo = ?", (mes, ativo))
    dadosativo = cursor.fetchall()
    print(dadosativo)
    adicionar = True
    for d in dadosativo:
        if d[1] == tpearn and d[3] == valor_u:
            # verifica se o dividendo ja esta no banco de dados
            adicionar = False
            break
    return adicionar

def visualizao_carteira():
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            W.Ativo,
            W.Quantidade,
            W.ValorTotal,
            CV.VTAtual,
            CV.Diferenca,
            CV.Data
        FROM Wallet W
        JOIN CurrentValue CV
            ON CV.Ativo = W.Ativo
        WHERE CV.Data = (
            SELECT MAX(CV2.Data)
            FROM CurrentValue CV2
            WHERE CV2.Ativo = W.Ativo
        )
    """)
    dados = cursor.fetchall()
    conexao.commit()
    conexao.close()
    return dados

# u -> Update -> Opcional incialmente

# D -> Delete

def del_cow(table, ID):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE ID = ?", (ID,))
    conexao.commit()
    conexao.close()

def del_all_cow(table):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {table}")
    conexao.commit()
    conexao.close()

#print(read_table("Wallet"))
#visualizao_carteira()
#del_all_cow("Earnings")