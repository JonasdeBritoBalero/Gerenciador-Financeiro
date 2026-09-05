from datetime import datetime
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
def inserir_ordem(ativo, tpativo, ordem, quant, valor, data=None):
    
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

# u -> Update -> Opcional incialmente

# D -> Delete

def del_cow(table, ID):
    conexao = sqlite3.connect("Finanças.db")
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE ID = ?", (ID,))
    conexao.commit()
    conexao.close()



#print(read_table("Wallet"))