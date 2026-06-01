import os
from flask import Flask, render_template, request, redirect
import json
import re
from datetime import datetime

app = Flask(__name__)
print("RODANDO APP DE:", os.path.abspath(__file__))
ARQUIVO = "chamados.json"


# =========================
# JSON
# =========================
def carregar():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar(chamados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(chamados, f, indent=4, ensure_ascii=False)


# =========================
# VALIDAÇÃO
# =========================
def validar_nome(nome):
    nome = nome.strip()

    if len(nome) == 0:
        return False

    if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome):
        return False

    palavras_invalidas = [
        "pc", "internet", "erro", "travando", "lento",
        "bug", "problema", "não funciona"
    ]

    nome_lower = nome.lower()

    if any(p in nome_lower for p in palavras_invalidas):
        return False

    return True


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return redirect("/chamados")


# =========================
# LISTAR CHAMADOS
# =========================
@app.route("/chamados")
def listar():
    chamados = carregar()
    return render_template("listar.html", chamados=chamados)


# =========================
# CRIAR CHAMADO
# =========================
@app.route("/criar", methods=["GET", "POST"])
def criar():

    if request.method == "POST":

        solicitante = request.form["solicitante"]

        if not validar_nome(solicitante):
            return "Nome inválido"

        descricao = request.form["descricao"]

        if len(descricao.strip()) < 10:
            return "A descrição deve ter pelo menos 10 caracteres."

        chamados = carregar()

        numero_chamado = (
            f"CH-{datetime.now().strftime('%Y%m%d')}-"
            f"{len(chamados)+1:03d}"
        )

        chamado = {
            "id": numero_chamado,
            "solicitante": solicitante,
            "titulo": request.form["titulo"],
            "descricao": descricao,
            "prioridade": request.form["prioridade"],
            "tecnico": "Não atribuído",
            "status": "Aberto",
            "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        chamados.append(chamado)
        salvar(chamados)

        return redirect("/chamados")

    return render_template("criar.html")


# =========================
# ALTERAR STATUS
# =========================
@app.route("/status/<int:id>/<novo_status>")
def status(id, novo_status):

    chamados = carregar()

    if 0 <= id < len(chamados):
        chamados[id]["status"] = novo_status
        salvar(chamados)

    return redirect("/chamados")


# =========================
# EXCLUIR CHAMADO
# =========================
@app.route("/excluir/<int:id>")
def excluir(id):

    chamados = carregar()

    if 0 <= id < len(chamados):
        chamados.pop(id)
        salvar(chamados)

    return redirect("/chamados")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
