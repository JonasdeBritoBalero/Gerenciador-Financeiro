from core.app import init
from data.crud import visualizao_carteira

# Menu:
def main():
    while True:
        carteira = visualizao_carteira()
        if carteira:
            print("-"*77)
            print(f"|{'Sua carteira de investimento':^75}|")
            print(f"|{'Ativo':^8}|{'Qt':^6}|{'Investido':^12}|{'Real':^12}|{'Diferen':^12}|{'Data':^20}|")
            print("-"*77)
            for a in carteira:
                print(f"|{a[0]:^8}|{a[1]:^6}|{a[2]:^12.2f}|{a[3]:^12.2f}|{a[4]:^12}|{a[5]:^20}|")
        print("""Bem vindo ao Gerenciador Financeiro!
O que deseja fazer:
1 - Atualização dos ativos.
2 - Compra de ativos.
3 - Venda de ativos.
4 - Sair.""")
        opcao = int(input("Opção:"))
        continuar = init(opcao)

        if not continuar:
            break

if __name__ == "__main__":
    main()
    #ativos = {"MXRF11": 9.74}
    #tratamento_dados_atual(ativos)

# Passo 1: Pegar os valores atuais dos ativos.