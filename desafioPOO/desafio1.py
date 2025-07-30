from abc import ABC, abstractmethod
from datetime import datetime

# ========================
# Cliente e Pessoa Física
# ========================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print("Conta não pertence a este cliente.")

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento


# ================
# Conta e Corrente
# ================

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(numero, cliente)
        cliente.adicionar_conta(conta)
        return conta

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
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False

        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False

        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False

        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado.")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        saques_realizados = len([
            t for t in self.historico.transacoes if t["tipo"] == "Saque"
        ])

        if saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False

        if valor > self.limite:
            print("Valor acima do limite por saque.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente.nome}"


# ============
# Histórico
# ============

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# ==================
# Transações (ABC)
# ==================

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
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# ======================
# Demonstração (teste)
# ======================

if __name__ == "__main__":
    # Criar cliente e conta
    cliente = PessoaFisica("Carlos Silva", "10/05/1990", "12345678900", "Rua Central, 123")
    conta = ContaCorrente.nova_conta(cliente, 1)

    # Operações
    cliente.realizar_transacao(conta, Deposito(1000))
    cliente.realizar_transacao(conta, Saque(200))
    cliente.realizar_transacao(conta, Saque(300))
    cliente.realizar_transacao(conta, Saque(600))  # Excede limite

    # Extrato
    print("\n=== Extrato ===")
    for t in conta.historico.transacoes:
        print(f"{t['data']} | {t['tipo']} | R$ {t['valor']:.2f}")

    print("\n" + str(conta))
