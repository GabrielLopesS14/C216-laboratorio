def _setup(client):
    """Cria uma conta e uma categoria (obrigatorias para a transacao)."""
    conta = client.post(
        "/api/v1/contas/",
        json={"nome": "Nubank", "tipo": "corrente", "saldo_inicial": 0},
    ).json()
    categoria = client.post(
        "/api/v1/categorias/",
        json={"nome": "Salario", "tipo": "receita"},
    ).json()
    return conta["id"], categoria["id"]

def _payload(conta_id, categoria_id, tag_ids=None, descricao="Salario"):
    return {
        "descricao": descricao,
        "valor": 1500.50,
        "data": "2024-01-15",
        "tipo": "receita",
        "conta_id": conta_id,
        "categoria_id": categoria_id,
        "tag_ids": tag_ids or [],
    }

def test_criar_transacao(client):
    cid, catid = _setup(client)
    resp = client.post("/api/v1/transacoes/", json=_payload(cid, catid))
    assert resp.status_code == 201
    assert resp.json()["descricao"] == "Salario"

def test_criar_transacao_com_tags(client):
    cid, catid = _setup(client)
    t1 = client.post("/api/v1/tags/", json={"nome": "trabalho"}).json()
    t2 = client.post("/api/v1/tags/", json={"nome": "fixo"}).json()
    resp = client.post(
        "/api/v1/transacoes/",
        json=_payload(cid, catid, tag_ids=[t1["id"], t2["id"]]),
    )
    assert resp.status_code == 201
    #Valida o relacionamento N:M: a transacao volta com as 2 tags.
    assert len(resp.json()["tags"]) == 2

def test_listar_transacoes(client):
    cid, catid = _setup(client)
    for i in range(3):
        client.post("/api/v1/transacoes/", json=_payload(cid, catid, descricao=f"Mov {i}"))
    resp = client.get("/api/v1/transacoes/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

def test_buscar_transacao(client):
    cid, catid = _setup(client)
    criada = client.post("/api/v1/transacoes/", json=_payload(cid, catid)).json()
    resp = client.get(f"/api/v1/transacoes/{criada['id']}")
    assert resp.status_code == 200
    #A resposta traz os objetos relacionados (conta e categoria).
    assert resp.json()["conta"]["id"] == cid
    assert resp.json()["categoria"]["id"] == catid

def test_atualizar_transacao(client):
    cid, catid = _setup(client)
    criada = client.post("/api/v1/transacoes/", json=_payload(cid, catid)).json()
    resp = client.put(
        f"/api/v1/transacoes/{criada['id']}",
        json=_payload(cid, catid, descricao="Editado"),
    )
    assert resp.status_code == 200
    assert resp.json()["descricao"] == "Editado"

def test_deletar_transacao(client):
    cid, catid = _setup(client)
    criada = client.post("/api/v1/transacoes/", json=_payload(cid, catid)).json()
    resp = client.delete(f"/api/v1/transacoes/{criada['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/v1/transacoes/{criada['id']}").status_code == 404
