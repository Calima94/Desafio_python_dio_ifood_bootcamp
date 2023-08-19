usuarios = []
numero_de_contas_criadas = 0
AGENCIA = "0001"

MENU = """
[c] Cadastrar cliente
[y] Cadastrar conta corrente 
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


def achar_usuario(usuarios: list):
    """
    Função tem como objetivo verificar se o usuario ja foi criado, ou seja, ja tem cpf cadastrado
    :param usuarios:
    :return: bool(True ou false), n(numero do usuario na lista), cpf(cpf do usuario), i(numero da conta corrente)
    """
    agencia = input("Digite o numero da agencia com quatro digitos\n")
    conta = int(input("digite o numero da conta\n"))
    for n, usuario in enumerate(usuarios):
        for cpf in usuario:
            cpf = str(cpf)
            for i, _ in enumerate(usuarios[n][cpf]["conta_corrente"]):
                agencia_achada = usuarios[n][cpf]["conta_corrente"][i]["agencia"] == agencia
                conta_achada = usuarios[n][cpf]["conta_corrente"][i]["numero_da_conta_corrente"] == conta
                if agencia_achada and conta_achada:
                    return True, n, cpf, i

    print("usuario nao encontrado redigite a agencia e o numero da conta corrente")

    return False, 0, 0, 0


def criar_novo_usuario(usuarios: list):
    """
    Função para cadastro das informacoes do usuario (exceto conta bancária)
    :param usuarios:
    :return: 0 (código para continuação do programa)
    """
    nome_completo = input("Digite o nome completo do usuario (sem abreviações)\n")
    data_de_nascimento = input("Digite a data de nascimento do usuário no formato xx/xx/xxxx -> exemplo 06/09/1974\n")
    cpf = input("Digite o CPF do cliente (apenas numeros)\n")
    usuario_encontrado = False
    for i, _ in enumerate(usuarios):
        if cpf == str(list(usuarios[i].keys())[0]):
            print("Usuario ja cadastrado, favor cadastre outro cpf")
            usuario_encontrado = True
    if usuario_encontrado:
        return 0
    logradouro = input(
        "Digite o nome da rua/avenida da residencia do cliente e o complemento se houver, exemplo -> rua abc, 327\n")
    bairro = input("Digite o bairro do cliente\n")
    cidade = input("Digite a Cidade do cliente\n")
    sigla_do_estado = input("Digite a sigla do estado do cliente\n")

    endereco_cliente = f"{logradouro} {bairro} {cidade} {sigla_do_estado}"
    conta_corrente = []
    usuario = {cpf: {"nome_completo": nome_completo,
                     "data_de_nascimento": data_de_nascimento,
                     "endereco_cliente": endereco_cliente,
                     "conta_corrente": conta_corrente}}
    usuarios.append(usuario)
    return 0


def cadastrar_conta_corrente(usuarios: list) -> int:
    """
    Função para cadastro de conta corrente para usuarios previamente cadastrados
    :param usuarios:
    :return: 0 (código para continuação do programa)
    """
    global numero_de_contas_criadas
    global AGENCIA
    cpf = input("Digite o cpf do usuario (somente numeros)\n")
    # print(cpf)
    # print(usuarios)
    for n, usuario in enumerate(usuarios):

        if cpf in usuario:
            numero_de_contas_criadas += 1
            saldo = 0
            limite_por_saque = 500
            extrato = ""
            numero_de_saques = 0
            LIMITE_DE_SAQUES = 3

            informacoes_da_conta_do_usuario = {"agencia": AGENCIA,
                                               "numero_da_conta_corrente": numero_de_contas_criadas,
                                               "saldo": saldo,
                                               "limite_por_saque": limite_por_saque,
                                               "extrato": extrato,
                                               "numero_de_saques": numero_de_saques,
                                               "limite_de_saques": LIMITE_DE_SAQUES}
            usuarios[n][cpf]["conta_corrente"].append(informacoes_da_conta_do_usuario)
            numero_de_contas_do_usuario = len(usuarios[n][cpf]["conta_corrente"])
            print(f"Conta criada com sucesso com a agencia:")
            print(usuarios[n][cpf]["conta_corrente"][numero_de_contas_do_usuario - 1]["agencia"])
            print("e conta corrente:")
            print(usuarios[n][cpf]["conta_corrente"][numero_de_contas_do_usuario - 1]["numero_da_conta_corrente"])
            return 0

    print("Nao foi possivel criar a conta, usuario nao possui cpf cadastrado, favor realizar cadastro do usuario")
    return 0


def deposito(saldo: float, extrato: str) -> float:
    """
    Função destinada a computar o valor a ser depositado se este for valido

    :param saldo:
    :param extrato:
    :return: valor (a ser depositado)
    """
    try:
        valor = float(input(f"Insira o valor a ser depositado:\n"))
        if valor <= 0:
            print("O valor do deposito precisa ser maior que 0\n")
            return 0.0
        return valor
    except ValueError:
        print("insira um valor valido\n")
        return 0.0


def deposito_menu(usuarios: list) -> int:
    """
    Menu que atualiza o extrato e saldo do cliente caso seja realizado um valor de deposito valido
    :param usuarios:
    :return: 0 (código para continuação do programa)
    """
    usuario_valido, n, cpf, i = achar_usuario(usuarios)
    if usuario_valido:
        saldo = usuarios[n][cpf]["conta_corrente"][i]["saldo"]
        extrato = usuarios[n][cpf]["conta_corrente"][i]["extrato"]
        valor = deposito(saldo, extrato)
        usuarios[n][cpf]["conta_corrente"][i]["saldo"] += valor
        usuarios[n][cpf]["conta_corrente"][i]["extrato"] += f"Deposito realizado de R${valor:.2f}\n"
    return 0


def saque(saldo: float, limite_por_saque: float) -> (bool, float):
    """
        Função que realiza a checagem se o valor de saque é valido,

        :param saldo, limite_por_saque
        :return: bool(valido, ou invalido), valor_a_ser_sacado(valor digitado ou 0 caso valor invalido)
        """
    try:
        valor_a_ser_sacado = float(input(f"Insira o valor a ser sacado:\n"))
        if valor_a_ser_sacado <= 0:
            print("O valor do saque precisa ser maior que 0\n")
            return False, 0

        if valor_a_ser_sacado > limite_por_saque:
            print(f"O valor de retirada máximo por saque é de R${limite_por_saque:.2f}\n")
            return False, 0

        if valor_a_ser_sacado > saldo:
            print(f"O valor de saque nao pode ser realizado pois e maior que o valor do saldo\n")
            return False, 0

        return True, valor_a_ser_sacado
    except ValueError:
        print("insira um valor valido\n")
        return False, 0


def saque_menu(usuarios: list) -> int:
    """
    Menu que atualiza o extrato e saldo do cliente caso seja realizado um valor de saque valido
    :param usuarios:
    :return: 0 (código para continuação do programa)
    """

    usuario_valido, n, cpf, i = achar_usuario(usuarios)
    if usuario_valido:
        saldo = usuarios[n][cpf]["conta_corrente"][i]["saldo"]
        limite_por_saque = usuarios[n][cpf]["conta_corrente"][i]["limite_por_saque"]
        numero_de_saques = usuarios[n][cpf]["conta_corrente"][i]["numero_de_saques"]
        limite_de_saques = usuarios[n][cpf]["conta_corrente"][i]["limite_de_saques"]
        if saldo == 0.0:
            print("Não sera possivel a realizacao do saque por falta de saldo")
            return 0
        if numero_de_saques >= limite_de_saques:
            print("Numero de saques realizados no dia maior que o permitido")
            return 0

        saque_realizado, valor_a_ser_sacado = saque(saldo=saldo,
                                                    limite_por_saque=limite_por_saque)
        if saque_realizado:
            usuarios[n][cpf]["conta_corrente"][i]["extrato"] += (f"Saque realizado de R${valor_a_ser_sacado:.2f}\n")
            usuarios[n][cpf]["conta_corrente"][i]["numero_de_saques"] += 1
            usuarios[n][cpf]["conta_corrente"][i]["saldo"] -= valor_a_ser_sacado
            return 0

    return 0


def extrato(saldo: float, extrato_: str) -> None:
    """
    Função que mostra o saldo do cliente
    :param saldo:
    :param extrato_:
    :return: None
    """
    if extrato_ == "":
        print("Nao foram realizados movimentacoes.")
    else:
        print(extrato_)
        print(type(extrato_))
    print(f"O saldo da conta e R${saldo:.2f}")


def extrato_menu(usuarios: list) -> int:
    """
    Menu que mostra o saldo do cliente
    :param usuarios:
    :return: 0 (código para continuação do programa)
    """

    usuario_valido, n, cpf, i = achar_usuario(usuarios)
    if usuario_valido:
        saldo = usuarios[n][cpf]["conta_corrente"][i]["saldo"]
        extrato_ = usuarios[n][cpf]["conta_corrente"][i]["extrato"]
        extrato(saldo, extrato_=extrato_)
    return 0


def quit_(usuarios: list) -> None:
    """
    Menu para sair do menu principal
    :param usuarios:
    :return: None
    """
    return None


OPCOES = {"c": criar_novo_usuario, "y": cadastrar_conta_corrente, "d": deposito_menu, "s": saque_menu,
          "e": extrato_menu, "q": quit_}

while True:
    opcao = input(MENU)
    codigo = 0
    try:
        codigo = OPCOES[opcao](usuarios)
    except KeyError:
        print("Opcao nao se encontra no menu")
    if codigo is None:
        break
