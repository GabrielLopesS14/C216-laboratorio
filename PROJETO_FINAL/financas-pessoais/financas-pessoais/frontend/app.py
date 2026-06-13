import os

import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "financas-pessoais-secret"

API_URL = os.getenv("API_URL", "http://backend:8000/api/v1")

def api_get(path):
    """GET resiliente: devolve [] se a API estiver fora do ar."""
    try:
        resp = requests.get(f"{API_URL}{path}", timeout=5)
        if resp.ok:
            return resp.json()
    except requests.RequestException:
        pass
    return []

def api_get_one(path):
    """GET de um unico recurso; devolve None em caso de falha."""
    try:
        resp = requests.get(f"{API_URL}{path}", timeout=5)
        if resp.ok:
            return resp.json()
    except requests.RequestException:
        pass
    return None

# Dashboard
@app.route("/")
def index():
    transacoes = api_get("/transacoes/")
    contas = api_get("/contas/")

    receitas = sum(float(t["valor"]) for t in transacoes if t["tipo"] == "receita")
    despesas = sum(float(t["valor"]) for t in transacoes if t["tipo"] == "despesa")
    saldo_inicial = sum(float(c["saldo_inicial"]) for c in contas)
    saldo = saldo_inicial + receitas - despesas

    ultimas = sorted(transacoes, key=lambda t: t["data"], reverse=True)[:5]

    return render_template(
        "index.html",
        saldo=saldo,
        receitas=receitas,
        despesas=despesas,
        ultimas=ultimas,
    )

#Transacoes
@app.route("/transacoes")
def transacoes():
    return render_template("transacoes.html", transacoes=api_get("/transacoes/"))

def _ler_form_transacao():
    return {
        "descricao": request.form["descricao"],
        "valor": float(request.form["valor"]),
        "data": request.form["data"],
        "tipo": request.form["tipo"],
        "conta_id": int(request.form["conta_id"]),
        "categoria_id": int(request.form["categoria_id"]),
        "tag_ids": [int(t) for t in request.form.getlist("tag_ids")],
    }

@app.route("/transacoes/nova", methods=["GET", "POST"])
def nova_transacao():
    if request.method == "POST":
        resp = requests.post(f"{API_URL}/transacoes/", json=_ler_form_transacao())
        if resp.status_code == 201:
            flash("Transacao criada com sucesso!", "success")
            return redirect(url_for("transacoes"))
        flash("Erro ao criar transacao.", "danger")

    return render_template(
        "transacao_form.html",
        transacao=None,
        contas=api_get("/contas/"),
        categorias=api_get("/categorias/"),
        tags=api_get("/tags/"),
    )

@app.route("/transacoes/<int:transacao_id>/editar", methods=["GET", "POST"])
def editar_transacao(transacao_id):
    if request.method == "POST":
        resp = requests.put(
            f"{API_URL}/transacoes/{transacao_id}", json=_ler_form_transacao()
        )
        if resp.ok:
            flash("Transacao atualizada!", "success")
            return redirect(url_for("transacoes"))
        flash("Erro ao atualizar transacao.", "danger")

    return render_template(
        "transacao_form.html",
        transacao=api_get_one(f"/transacoes/{transacao_id}"),
        contas=api_get("/contas/"),
        categorias=api_get("/categorias/"),
        tags=api_get("/tags/"),
    )

@app.route("/transacoes/<int:transacao_id>/excluir")
def excluir_transacao(transacao_id):
    requests.delete(f"{API_URL}/transacoes/{transacao_id}")
    flash("Transacao removida.", "info")
    return redirect(url_for("transacoes"))

#Contas
@app.route("/contas", methods=["GET", "POST"])
def contas():
    if request.method == "POST":
        payload = {
            "nome": request.form["nome"],
            "tipo": request.form["tipo"],
            "saldo_inicial": float(request.form.get("saldo_inicial") or 0),
        }
        requests.post(f"{API_URL}/contas/", json=payload)
        flash("Conta adicionada!", "success")
        return redirect(url_for("contas"))
    return render_template("contas.html", contas=api_get("/contas/"))

@app.route("/contas/<int:conta_id>/excluir")
def excluir_conta(conta_id):
    requests.delete(f"{API_URL}/contas/{conta_id}")
    flash("Conta removida.", "info")
    return redirect(url_for("contas"))

#Categorias
@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    if request.method == "POST":
        payload = {"nome": request.form["nome"], "tipo": request.form["tipo"]}
        requests.post(f"{API_URL}/categorias/", json=payload)
        flash("Categoria adicionada!", "success")
        return redirect(url_for("categorias"))
    return render_template("categorias.html", categorias=api_get("/categorias/"))

@app.route("/categorias/<int:categoria_id>/excluir")
def excluir_categoria(categoria_id):
    requests.delete(f"{API_URL}/categorias/{categoria_id}")
    flash("Categoria removida.", "info")
    return redirect(url_for("categorias"))

@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "POST":
        requests.post(f"{API_URL}/tags/", json={"nome": request.form["nome"]})
        flash("Tag adicionada!", "success")
        return redirect(url_for("tags"))
    return render_template("tags.html", tags=api_get("/tags/"))


@app.route("/tags/<int:tag_id>/excluir")
def excluir_tag(tag_id):
    requests.delete(f"{API_URL}/tags/{tag_id}")
    flash("Tag removida.", "info")
    return redirect(url_for("tags"))

#Relatorios
@app.route("/relatorios")
def relatorios():
    transacoes = api_get("/transacoes/")
    por_categoria = {}
    for t in transacoes:
        if t["tipo"] != "despesa":
            continue
        nome = t["categoria"]["nome"] if t.get("categoria") else "Sem categoria"
        por_categoria[nome] = por_categoria.get(nome, 0) + float(t["valor"])

    dados = sorted(por_categoria.items(), key=lambda x: x[1], reverse=True)
    total = sum(valor for _, valor in dados)
    return render_template("relatorios.html", dados=dados, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
