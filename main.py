from core.app import tratamento_dados_atual, init

# Menu:
def main():
    while True:
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