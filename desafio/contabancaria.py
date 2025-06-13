menu_principal = """
[c] Criar conta
[l] Login
[s] Sair

Escolha uma opção: """

menu_conta = """
[a] Adicionar dinheiro
[r] Retirar dinheiro
[x] Extrato bancário
[o] Logout

Escolha uma opção: """

banco = {}  # {numero_conta: {"senha": senha, "saldo": saldo, "registro": movimentacoes}}

def criar_conta():
    numero = input("Digite o número da conta: ")
    if numero in banco:
        print("Conta já existe!")
        return
    senha = input("Crie uma senha para sua conta: ")  # senha visível aqui
    banco[numero] = {"senha": senha, "saldo": 0.0, "registro": ""}
    print(f"Conta {numero} criada com sucesso!")

def login():
    numero = input("Número da conta: ")
    if numero not in banco:
        print("Conta não encontrada.")
        return None
    senha = input("Senha: ")  # senha visível aqui
    if senha != banco[numero]["senha"]:
        print("Senha incorreta.")
        return None
    print(f"Bem-vindo, conta {numero}!")
    return numero

def operacoes_conta(numero):
    while True:
        escolha = input(menu_conta).lower()
        conta = banco[numero]
        if escolha == "a":
            try:
                deposito = float(input("Quanto deseja depositar? R$ "))
                if deposito > 0:
                    conta["saldo"] += deposito
                    conta["registro"] += f"Depósito efetuado: R$ {deposito:.2f}\n"
                    print("Valor depositado com sucesso!")
                else:
                    print("Valor inválido para depósito!")
            except ValueError:
                print("Valor inválido!")
        elif escolha == "r":
            try:
                saque = float(input("Quanto deseja sacar? R$ "))
                if saque > 0 and saque <= conta["saldo"]:
                    conta["saldo"] -= saque
                    conta["registro"] += f"Saque efetuado: R$ {saque:.2f}\n"
                    print("Saque realizado com sucesso!")
                elif saque > conta["saldo"]:
                    print("Saldo insuficiente para saque!")
                else:
                    print("Valor inválido para saque!")
            except ValueError:
                print("Valor inválido!")
        elif escolha == "x":
            print("\n***** EXTRATO BANCÁRIO *****")
            if conta["registro"]:
                print(conta["registro"])
            else:
                print("Nenhuma transação registrada.")
            print(f"Saldo disponível: R$ {conta['saldo']:.2f}")
        elif escolha == "o":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida! Tente novamente.")

def iniciar_sistema():
    while True:
        escolha = input(menu_principal).lower()
        if escolha == "c":
            criar_conta()
        elif escolha == "l":
            conta_logada = login()
            if conta_logada:
                operacoes_conta(conta_logada)
        elif escolha == "s":
            print("Encerrando o sistema. Obrigado por utilizar!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    iniciar_sistema()
