saldo = 0
limite_por_saque = 500
extrato = ""
numero_de_saques = 0
LIMITE_DE_SAQUES = 3

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

informacoes_usuario = {"saldo": saldo,
                       "limite_por_saque": limite_por_saque,
                       "extrato": extrato,
                       "numero_de_saques": numero_de_saques,
                       "limite_de_saques": LIMITE_DE_SAQUES}


def deposito(informacoes_usuario):
    try:
        valor = float(input(f"Insira o valor a ser depositado:\n"))
        if valor <= 0:
            print("O valor do deposito precisa ser maior que 0")
            return 0.0, informacoes_usuario
        informacoes_usuario["extrato"] += f"Deposito realizado de R${valor:.2f}\n"
        return valor, informacoes_usuario
    except ValueError:
        print("insira um valor valido")
        return 0.0, informacoes_usuario


def saque(informacoes_usuario):
    try:
        if informacoes_usuario["saldo"] == 0.0:
            print("Não sera possivel a realizacao do saque por falta de saldo")
            return 0.0, informacoes_usuario

        if informacoes_usuario["numero_de_saques"] >= informacoes_usuario["limite_de_saques"]:
            print("Numero de saques realizados no dia maior que o permitido")
            return 0.0, informacoes_usuario

        valor_a_ser_sacado = float(input(f"Insira o valor a ser sacado:\n"))
        if valor_a_ser_sacado <= 0:
            print("O valor do saque precisa ser maior que 0")
            return 0.0, informacoes_usuario

        if valor_a_ser_sacado > limite_por_saque:
            print(f"O valor de retirada máximo por saque é de R${limite_por_saque:.2f}")
            return 0.0, informacoes_usuario

        if valor_a_ser_sacado > informacoes_usuario["saldo"]:
            print(f"O valor de saque nao pode ser realizado pois e maior que o valor do saldo")
            return 0.0, informacoes_usuario

        informacoes_usuario["extrato"] += (f"Saque realizado de R${valor_a_ser_sacado:.2f}\n")
        informacoes_usuario["numero_de_saques"] += 1
        valor_a_ser_sacado = -1 * valor_a_ser_sacado

        return valor_a_ser_sacado, informacoes_usuario

    except ValueError:
        print("insira um valor valido")
        return 0.0, informacoes_usuario


def extrato(informacoes_usuario):
    if informacoes_usuario["extrato"] == "":
        print("Nao foram realizados movimentacoes.")
        print(f"O saldo da conta e R${informacoes_usuario['saldo']:.2f}")
        return 0.0, informacoes_usuario
    print(informacoes_usuario["extrato"])
    print(f"O saldo da conta e R${informacoes_usuario['saldo']:.2f}")
    return 0.0, informacoes_usuario


def quit_(informacoes_usuario):
    return None, informacoes_usuario


OPCOES = {"d": deposito, "s": saque, "e": extrato, "q": quit_}

while True:
    opcao = input(menu)
    try:
        variacao_de_saldo, informacoes_usuario = OPCOES[opcao](informacoes_usuario)
    except KeyError:
        variacao_de_saldo = 0
        print("Opcao nao se encontra no menu")

    if variacao_de_saldo is None:
        break
    informacoes_usuario["saldo"] += variacao_de_saldo
