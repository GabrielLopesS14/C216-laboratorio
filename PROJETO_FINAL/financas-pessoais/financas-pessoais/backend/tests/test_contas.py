def _payload(nome="Nubank"):
    return {"nome": nome, "tipo": "corrente", "saldo_inicial": 100}

def test_criar_conta(client):
    resp = client.post("/api/v1/contas/", json=_payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == "Nubank"
    assert "id" in body

def test_listar_contas(client):
    client.post("/api/v1/contas/", json=_payload("Conta 1"))
    client.post("/api/v1/contas/", json=_payload("Conta 2"))
    client.post("/api/v1/contas/", json=_payload("Conta 3"))
    resp = client.get("/api/v1/contas/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

def test_buscar_conta(client):
    criada = client.post("/api/v1/contas/", json=_payload()).json()
    resp = client.get(f"/api/v1/contas/{criada['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == criada["id"]

def test_buscar_conta_inexistente(client):
    resp = client.get("/api/v1/contas/9999")
    assert resp.status_code == 404

def test_atualizar_conta(client):
    criada = client.post("/api/v1/contas/", json=_payload()).json()
    resp = client.put(f"/api/v1/contas/{criada['id']}", json=_payload("Nubank Editado"))
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Nubank Editado"

def test_deletar_conta(client):
    criada = client.post("/api/v1/contas/", json=_payload()).json()
    resp = client.delete(f"/api/v1/contas/{criada['id']}")
    assert resp.status_code == 200
    # Apos deletar, a busca deve retornar 404.
    assert client.get(f"/api/v1/contas/{criada['id']}").status_code == 404
