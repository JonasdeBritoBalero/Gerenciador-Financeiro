
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
        if opcao == 1:
            pass
        elif opcao == 2:
            pass
        elif opcao == 3:
            pass
        elif opcao == 4:
            print("Saindo do Gerenciador Financeiro!")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()

# Passo 1: Pegar os valores atuais dos ativos.