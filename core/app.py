from WebScraping.scraper import pegar_ativo_completo
from data.crud import read_nome_ativos, read_table, inserir_atual, inserir_ordem, inserir_dividendo
from sheets.sheets import Inserir_dividendos_sheets, atualizacao_ativos

def init(opc):
    if opc == 1: # Atualizacao dos dados dos ativos
        nomes_ativos = read_nome_ativos() # pega os ativos que estão na carteira
        preco, dividendo = pegar_ativo_completo(nomes_ativos) # pegas o preco e os dividendos dos ativos
        atualizacao_ativos(preco)
        current = tratamento_dados_atual(preco) # valores formatados para serem inseridos no banco
        for a, d in current.items():
            inserir_atual(a, d["ValorU"], d["ValorR"], d["diferenca"])
        
        calculando_earn(dividendo)
        
        return True
    elif opc == 2: # Compra de ativos
        nativos = read_nome_ativos()
        print("Ativos:")
        for a in nativos:
            print(f"-> {a}")
        ativo = str(input("Qual ativo você comprou ? "))
        ordem = 'C'
        quant = int(input("Quantas cotas você comprou? "))
        valor = float(input("Valor total da compra: R$ "))
        data = str(input("você efetuou a operação quando? (AAAA-MM-DD)"))
        print("app - ", data)
        inserir_ordem(ativo, ordem, quant, valor, data)
        return True
    elif opc == 3: # venda de ativos
        nativos = read_nome_ativos()
        print("Ativos:")
        for a in nativos:
            print(f"-> {a}")
        ativo = str(input("Qual ativo você vendeu ? "))
        tpativo = "" # FII ou Ação
        ordem = 'V'
        quant = int(input("Quantas cotas você vendeu? "))
        valor = float(input("Valor total da venda: R$ "))
        data = str(input("você efetuou a operação quando? (AAAA-MM-DD)"))
        inserir_ordem(ativo, tpativo, ordem, quant, valor, data)
        return True
    elif opc == 4:
        print("Saindo do sistema!")
        return False
    else:
        print("Opção errada!")
        return True



# Ativos = {"MXRF11": 9.74}
def tratamento_dados_atual(ativos):
    carteira = read_table("Wallet")
    print(carteira)
    atualizacao = {}
    for a, v in ativos.items():
        print(a, v)
        for ativo in carteira:
            if ativo[1] == a:
                valorI = round(ativo[3], 2) # total investido na carteira
                valorR = round(ativo[4] * v, 2) # quant da carteira * o valor atual do ativo
                diferenca = round(valorR - valorI, 2) # verifica a diferença de patrimonio, se teve prejuizo ou lucro e calcula
                atualizacao[a] = {"ValorU": v, "ValorI": valorI, "ValorR": valorR, "diferenca": diferenca}
                break
    return atualizacao


def calculando_earn(dividendo):
    # dividendo = {'TAEE4': [['JSCP', '2026-11-26', 0.11982486], ['Dividendos', '2026-11-26', 0.08025458]]}
    # Ativo, TpAtivo, TpEarnings, DataPag, ProUnitario, proTotal
    if dividendo:
        carteira = read_table("wallet")
        for a, v in dividendo.items():
            # a = nome do ativo
            # v = dividendos do ativos em uma lista, já que pode existir mais que 1 dividendo
            for c in carteira:
                # c = informação do ativo registrado na carteira
                if a == c[1]:
                    for n in v:
                        if n[0] == "JSCP":
                            valor = (n[2] * c[4]) * 0.825
                        else:
                            valor = n[2] * c[4]
                        inserir_dividendo(a, n[0], n[1], n[2], valor)
                        #Inserir_dividendos_sheets(a, n[1], valor)

        # [(1, 'MXRF11', 'FII', 10019.51, 1031, 9.72), (2, 'VRTA11', 'FII', 5964.01, 74, 80.59)]
        
    else:
        return print("Não teve nenhum dividendo!")
    print(carteira)
    '''for ativo, values in dividendo.items():
        for e in values:
            
    read_table("Earnings")'''

#ativos = {"MXRF11": 9.74}
#tratamento_dados_atual(ativos)