menu = """
[a] Adicionar dinheiro
[r] Retirar dinheiro
[x] Extrato bancário
[s] Sair

Escolha uma opção: """

saldo_atual = 0
registro_movimentacoes = ""

while True:
    escolha = input(menu).lower()

    if escolha == "a":
        deposito = float(input("Quanto deseja depositar? R$ "))
        if deposito > 0:
            saldo_atual += deposito
            registro_movimentacoes += f"Depósito efetuado: R$ {deposito:.2f}\n"
            print("Valor depositado com sucesso!")
        else:
            print("Valor inválido para depósito!")

    elif escolha == "r":
        saque = float(input("Quanto deseja sacar? R$ "))
        if saque > 0 and saque <= saldo_atual:
            saldo_atual -= saque
            registro_movimentacoes += f"Saque efetuado: R$ {saque:.2f}\n"
            print("Saque realizado com sucesso!")
        elif saque > saldo_atual:
            print("Saldo insuficiente para saque!")
        else:
            print("Valor inválido para saque!")

    elif escolha == "x":
        print("\n***** EXTRATO BANCÁRIO *****")
        if registro_movimentacoes:
            print(registro_movimentacoes)
        else:
            print("Nenhuma transação registrada.")
        print(f"Saldo disponível: R$ {saldo_atual:.2f}")

    elif escolha == "s":
        print("Encerrando o sistema. Obrigado por utilizar!")
        break

    else:
        print("Opção inválida! Tente novamente.")
