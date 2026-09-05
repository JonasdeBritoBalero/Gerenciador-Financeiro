from WebScraping.scraper import pegar_ativo_completo
from data.crud import read_nome_ativos, read_table, inserir_atual

def init(opc):
    if opc == 1:
        nomes_ativos = read_nome_ativos()
        preco, dividendo = pegar_ativo_completo(nomes_ativos)
        current = tratamento_dados_atual(preco) # valores formatados para serem inseridos no banco
        for a, d in current.items():
            inserir_atual(a, d["TpAtivo"], d["ValorU"], d["ValorR"], d["diferenca"])



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