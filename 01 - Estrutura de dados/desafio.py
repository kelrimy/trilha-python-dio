import textwrap

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(self)
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif self.valor > conta.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif conta.numero_saques >= conta.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.numero_saques += 1
            conta.historico.adicionar_transacao(self)
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
        self.limite = 500.0
        self.limite_saques = 3
        self.numero_saques = 0

    def saldo(self):
        return self.saldo

    def nova_conta(cliente, numero):
        return Conta(cliente, numero)

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = Conta(usuario, numero_conta)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = type(transacao).__name__
            valor = transacao.valor
            print(f"{tipo}:\tR$ {valor:.2f}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                exibir_extrato(conta)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta("0001", numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
