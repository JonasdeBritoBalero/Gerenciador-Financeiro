from WebScraping.scraper import pegar_ativo_completo
from data.crud import read_nome_ativos, read_table, inserir_atual, inserir_ordem

def init(opc):
    if opc == 1: # Atualizacao dos dados dos ativos
        nomes_ativos = read_nome_ativos()
        preco, dividendo = pegar_ativo_completo(nomes_ativos)
        current = tratamento_dados_atual(preco) # valores formatados para serem inseridos no banco
        for a, d in current.items():
            inserir_atual(a, d["TpAtivo"], d["ValorU"], d["ValorR"], d["diferenca"])
        
        return True
    elif opc == 2: # Compra de ativos
        ativo = str(input("Qual ativo você comprou ? "))
        tpativo = "" # FII ou Ação
        ordem = 'C'
        quant = int(input("Quantas cotas você comprou? "))
        valor = float(input("Valor total da compra: R$ "))
        data = str(input("você efetuou a operação quando? (AAAA-MM-DD)"))
        inserir_ordem(ativo, tpativo, ordem, quant, valor, data)
        return True
    elif opc == 3: # venda de ativos
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
                atualizacao[a] = {"TpAtivo": ativo[2],"ValorU": v, "ValorI": valorI, "ValorR": valorR, "diferenca": diferenca}
                break
    return atualizacao


#ativos = {"MXRF11": 9.74}
#tratamento_dados_atual(ativos)