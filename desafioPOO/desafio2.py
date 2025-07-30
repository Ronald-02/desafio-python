import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def executar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Pessoa(Usuario):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


class ContaBancaria:
    def __init__(self, numero, usuario):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "1234"
        self._usuario = usuario
        self._historico = HistoricoTransacoes()

    @classmethod
    def criar_conta(cls, usuario, numero):
        return cls(numero, usuario)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def usuario(self):
        return self._usuario

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n>>> Valor inválido para saque! <<<")
            return False

        if valor > self._saldo:
            print("\n>>> Saldo insuficiente para saque! <<<")
            return False

        self._saldo -= valor
        print("\n>>> Saque efetuado com sucesso! <<<")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n>>> Valor inválido para depósito! <<<")
            return False

        self._saldo += valor
        print("\n>>> Depósito efetuado com sucesso! <<<")
        return True


class ContaCorrente(ContaBancaria):
    def __init__(self, numero, usuario, limite=1000.0, max_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._max_saques = max_saques

    def sacar(self, valor):
        saques_realizados = len(
            [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
        )

        if saques_realizados >= self._max_saques:
            print("\n>>> Limite de saques diários atingido! <<<")
            return False

        if valor > self._limite:
            print("\n>>> Valor do saque ultrapassa o limite permitido! <<<")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
Agência:\t{self.agencia}
Conta:\t{self.numero}
Titular:\t{self.usuario.nome}
"""


class HistoricoTransacoes:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.registrar(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.registrar(self)


def exibir_menu():
    menu_texto = """
    =============== MENU ===============
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu_texto))


def encontrar_usuario(cpf, usuarios):
    encontrados = [u for u in usuarios if u.cpf == cpf]
    return encontrados[0] if encontrados else None


def selecionar_conta(usuario):
    if not usuario.contas:
        print("\n>>> Usuário não possui conta cadastrada! <<<")
        return None

    # Apenas retorna a primeira conta (pode ser melhorado para selecionar entre várias)
    return usuario.contas[0]


def realizar_deposito(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n>>> Usuário não encontrado! <<<")
        return

    try:
        valor = float(input("Valor para depósito: "))
    except ValueError:
        print("\n>>> Valor inválido! <<<")
        return

    transacao = Deposito(valor)
    conta = selecionar_conta(usuario)
    if conta:
        usuario.executar_transacao(conta, transacao)


def realizar_saque(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n>>> Usuário não encontrado! <<<")
        return

    try:
        valor = float(input("Valor para saque: "))
    except ValueError:
        print("\n>>> Valor inválido! <<<")
        return

    transacao = Saque(valor)
    conta = selecionar_conta(usuario)
    if conta:
        usuario.executar_transacao(conta, transacao)


def mostrar_extrato(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n>>> Usuário não encontrado! <<<")
        return

    conta = selecionar_conta(usuario)
    if not conta:
        return

    print("\n======= EXTRATO =======")
    if not conta.historico.transacoes:
        print("Nenhuma movimentação realizada.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("=======================\n")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    if encontrar_usuario(cpf, usuarios):
        print("\n>>> Usuário com este CPF já existe! <<<")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço completo: ")

    novo_usuario = Pessoa(nome, nascimento, cpf, endereco)
    usuarios.append(novo_usuario)
    print("\n>>> Usuário criado com sucesso! <<<")


def criar_conta(numero, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = encontrar_usuario(cpf, usuarios)
    if not usuario:
        print("\n>>> Usuário não encontrado. Conta não criada. <<<")
        return

    conta = ContaCorrente.criar_conta(usuario, numero)
    contas.append(conta)
    usuario.adicionar_conta(conta)
    print("\n>>> Conta criada com sucesso! <<<")


def listar_contas(contas):
    if not contas:
        print("\n>>> Nenhuma conta cadastrada. <<<")
        return

    for conta in contas:
        print("=" * 50)
        print(conta)


def main():
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            realizar_deposito(usuarios)
        elif opcao == "s":
            realizar_saque(usuarios)
        elif opcao == "e":
            mostrar_extrato(usuarios)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero = len(contas) + 1
            criar_conta(numero, usuarios, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Obrigado por usar nosso sistema. Até logo!")
            break
        else:
            print("\n>>> Opção inválida! Tente novamente. <<<")


if __name__ == "__main__":
    main()
