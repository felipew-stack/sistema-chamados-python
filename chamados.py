import json
from datetime import datetime

ARQUIVO = "chamados.json"

try:
    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        chamados = json.load(arquivo)
except (FileNotFoundError, json.JSONDecodeError):
    chamados = []


def salvar_chamados():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(chamados, arquivo, indent=4, ensure_ascii=False)


while True:

    print("\n===== SISTEMA DE CHAMADOS =====")
    print("1 - Criar chamado")
    print("2 - Listar chamados")
    print("3 - Alterar status")
    print("4 - Excluir chamado")
    print("5 - Dashboard")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        solicitante = input("Nome do solicitante: ")
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

    elif opcao == "2":

        if len(chamados) == 0:
            print("\nNenhum chamado cadastrado.")

        else:

            print("\n===== LISTA DE CHAMADOS =====")

            for indice, chamado in enumerate(chamados):

                print(f"\nID: {indice}")
                print(f"Solicitante: {chamado['solicitante']}")
                print(f"Título: {chamado['titulo']}")
                print(f"Descrição: {chamado['descricao']}")
                print(f"Prioridade: {chamado['prioridade']}")
                print(f"Técnico: {chamado['tecnico']}")
                print(f"Status: {chamado['status']}")
                print(f"Data: {chamado['data_abertura']}")

    elif opcao == "3":

        if len(chamados) == 0:
            print("\nNenhum chamado cadastrado.")

        else:

            print("\n===== ALTERAR STATUS =====")

            for indice, chamado in enumerate(chamados):
                print(
                    f"ID {indice} - {chamado['titulo']} ({chamado['status']})"
                )

            try:
                id_chamado = int(
                    input("\nDigite o ID do chamado: ")
                )

                novo_status = input(
                    "Novo status (Aberto, Em Atendimento ou Resolvido): "
                )

                chamados[id_chamado]["status"] = novo_status

                salvar_chamados()

                print("\nStatus atualizado com sucesso!")

            except (ValueError, IndexError):
                print("\nID inválido!")

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
                    f"\nChamado '{removido['titulo']}' removido com sucesso!"
                )

            except (ValueError, IndexError):
                print("\nID inválido!")

    elif opcao == "5":

        total = len(chamados)

        abertos = sum(
            1 for chamado in chamados
            if chamado["status"] == "Aberto"
        )

        atendimento = sum(
            1 for chamado in chamados
            if chamado["status"] == "Em Atendimento"
        )

        resolvidos = sum(
            1 for chamado in chamados
            if chamado["status"] == "Resolvido"
        )

        print("\n===== DASHBOARD =====")
        print(f"Total de chamados: {total}")
        print(f"Abertos: {abertos}")
        print(f"Em Atendimento: {atendimento}")
        print(f"Resolvidos: {resolvidos}")

    elif opcao == "6":

        print("\nEncerrando sistema...")
        break

    else:

        print("\nOpção inválida!")
