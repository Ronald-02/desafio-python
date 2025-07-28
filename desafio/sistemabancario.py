import textwrap

# Dados simulando o "banco"
usuarios = []
contas = []

# Função para encontrar usuário por CPF
def buscar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

# Função para cadastrar novo usuário
def cadastrar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    usuario = buscar_usuario(cpf)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (rua, número - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário cadastrado com sucesso!")

# Função para criar conta vinculada a um CPF
def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    usuario = buscar_usuario(cpf)

    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")
        return

    numero_conta = len(contas) + 1
    contas.append({
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "saques": 0
    })

    print(f"Conta criada com sucesso! Agência: 0001 Conta: {numero_conta}")

# Função para realizar depósito
def depositar(conta):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido.")

# Função para realizar saque
def sacar(conta):
    valor = float(input("Informe o valor do saque: "))
    limite = 500
    limite_saques = 3

    if valor <= 0:
        print("Valor inválido.")
    elif valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor > limite:
        print("Valor excede o limite por saque.")
    elif conta["saques"] >= limite_saques:
        print("Número de saques diário excedido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["saques"] += 1
        print("Saque realizado com sucesso!")

# Função para exibir extrato
def mostrar_extrato(conta):
    print("\n======= EXTRATO =======")
    print(conta["extrato"] if conta["extrato"] else "Não foram realizadas movimentações.")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
    print("========================")

# Função para escolher conta por CPF
def selecionar_conta():
    cpf = input("Informe o CPF do titular: ")
    contas_do_usuario = [c for c in contas if c["usuario"]["cpf"] == cpf]

    if not contas_do_usuario:
        print("Nenhuma conta encontrada para este CPF.")
        return None

    if len(contas_do_usuario) == 1:
        return contas_do_usuario[0]
    
    print("Usuário possui múltiplas contas. Selecione:")
    for i, conta in enumerate(contas_do_usuario, start=1):
        print(f"{i} - Agência: {conta['agencia']} Conta: {conta['numero']}")

    escolha = int(input("Número da conta: ")) - 1
    return contas_do_usuario[escolha]

# Menu principal
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar usuário
[c] Criar conta
[q] Sair

=> """

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        conta = selecionar_conta()
        if conta:
            depositar(conta)

    elif opcao == "s":
        conta = selecionar_conta()
        if conta:
            sacar(conta)

    elif opcao == "e":
        conta = selecionar_conta()
        if conta:
            mostrar_extrato(conta)

    elif opcao == "u":
        cadastrar_usuario()

    elif opcao == "c":
        criar_conta()

    elif opcao == "q":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida.")
