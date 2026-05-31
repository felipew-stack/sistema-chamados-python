import json
import re
from datetime import datetime

ARQUIVO = "chamados.json"

try:
    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        chamados = json.load(arquivo)
except (FileNotFoundError, json.JSONDecodeError):
    chamados = []


# =========================
# VALIDAÇÃO DE NOME
# =========================
def validar_nome(nome):
    nome = nome.strip()

    if len(nome) == 0:
        return False

    # apenas letras e espaços
    if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome):
        return False

    # bloqueio de palavras que indicam problema (evita erro no campo)
    palavras_invalidas = [
        "pc", "internet", "erro", "travando", "lento",
        "não funciona", "bug", "problema"
    ]

    nome_lower = nome.lower()

    if any(p in nome_lower for p in palavras_invalidas):
        return False

    return True


def salvar_chamados():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(chamados, arquivo, indent=4, ensure_ascii=False)


def listar_chamados(filtro_status=None):
    if len(chamados) == 0:
        print("\nNenhum chamado cadastrado.")
        return

    print("\n===== LISTA DE CHAMADOS =====")

    for indice, chamado in enumerate(chamados):

        if filtro_status and chamado["status"] != filtro_status:
            continue

        print(f"\nID: {indice}")
        print(f"Solicitante: {chamado['solicitante']}")
        print(f"Título: {chamado['titulo']}")
        print(f"Descrição: {chamado['descricao']}")
        print(f"Prioridade: {chamado['prioridade']}")
        print(f"Técnico: {chamado['tecnico']}")
        print(f"Status: {chamado['status']}")
        print(f"Data: {chamado['data_abertura']}")


def buscar_chamados():
    termo = input("\nDigite título ou solicitante: ").lower()

    encontrados = []

    for indice, chamado in enumerate(chamados):
        if termo in chamado["titulo"].lower() or termo in chamado["solicitante"].lower():
            encontrados.append((indice, chamado))

    if not encontrados:
        print("\nNenhum chamado encontrado.")
        return

    print("\n===== RESULTADOS DA BUSCA =====")

    for indice, chamado in encontrados:
        print(f"\nID: {indice}")
        print(f"Título: {chamado['titulo']}")
        print(f"Solicitante: {chamado['solicitante']}")
        print(f"Status: {chamado['status']}")


# =========================
# MENU PRINCIPAL
# =========================
while True:

    print("\n===== SISTEMA DE CHAMADOS =====")
    print("1 - Criar chamado")
    print("2 - Listar chamados")
    print("3 - Alterar status")
    print("4 - Excluir chamado")
    print("5 - Dashboard")
    print("6 - Sair")
    print("7 - Buscar chamados")

    opcao = input("Escolha uma opção: ")

    # =========================
    # CRIAR CHAMADO
    # =========================
    if opcao == "1":

        # validação do nome
        while True:
            solicitante = input("Nome do solicitante: ")

            if validar_nome(solicitante):
                break
            else:
                print("\nNome inválido! Digite apenas um nome (ex: João Silva).")

        titulo = input("Título do chamado: ")
        descricao = input("Descrição do problema: ")
        prioridade = input("Prioridade (Baixa, Média ou Alta): ")
        tecnico = input("Técnico responsável: ")

        chamado = {
            "solicitante": solicitante,
            "titulo": titulo,
            "descricao": descricao,
            "prioridade": prioridade,
            "tecnico": tecnico,
            "status": "Aberto",
            "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        chamados.append(chamado)
        salvar_chamados()

        print("\nChamado criado com sucesso!")

    # =========================
    # LISTAR
    # =========================
    elif opcao == "2":

        print("\n1 - Ver todos")
        print("2 - Filtrar por status")

        escolha = input("Escolha: ")

        if escolha == "1":
            listar_chamados()

        elif escolha == "2":
            status = input("Status (Aberto, Em Atendimento, Resolvido): ")
            listar_chamados(status)

    # =========================
    # ALTERAR STATUS
    # =========================
    elif opcao == "3":

        if len(chamados) == 0:
            print("\nNenhum chamado cadastrado.")

        else:

            print("\n===== ALTERAR STATUS =====")

            for indice, chamado in enumerate(chamados):
                print(
                    f"ID {indice} - {chamado['titulo']} ({chamado['status']})")

            try:
                id_chamado = int(input("\nDigite o ID do chamado: "))

                novo_status = input(
                    "Novo status (Aberto, Em Atendimento ou Resolvido): "
                )

                chamados[id_chamado]["status"] = novo_status

                salvar_chamados()

                print("\nStatus atualizado com sucesso!")

            except (ValueError, IndexError):
                print("\nID inválido!")

    # =========================
    # EXCLUIR
    # =========================
    elif opcao == "4":

        if len(chamados) == 0:
            print("\nNenhum chamado cadastrado.")

        else:

            for indice, chamado in enumerate(chamados):
                print(f"ID {indice} - {chamado['titulo']}")

            try:

                id_chamado = int(
                    input("\nDigite o ID do chamado que deseja excluir: ")
                )

                removido = chamados.pop(id_chamado)

                salvar_chamados()

                print(
                    f"\nChamado '{removido['titulo']}' removido com sucesso!")

            except (ValueError, IndexError):
                print("\nID inválido!")

    # =========================
    # DASHBOARD
    # =========================
    elif opcao == "5":

        total = len(chamados)

        abertos = sum(
            1 for chamado in chamados if chamado["status"] == "Aberto")
        atendimento = sum(
            1 for chamado in chamados if chamado["status"] == "Em Atendimento")
        resolvidos = sum(
            1 for chamado in chamados if chamado["status"] == "Resolvido")

        print("\n===== DASHBOARD =====")
        print(f"Total de chamados: {total}")
        print(f"Abertos: {abertos}")
        print(f"Em Atendimento: {atendimento}")
        print(f"Resolvidos: {resolvidos}")

    # =========================
    # SAIR
    # =========================
    elif opcao == "6":
        print("\nEncerrando sistema...")
        break

    # =========================
    # BUSCA
    # =========================
    elif opcao == "7":
        buscar_chamados()

    else:
        print("\nOpção inválida!")
