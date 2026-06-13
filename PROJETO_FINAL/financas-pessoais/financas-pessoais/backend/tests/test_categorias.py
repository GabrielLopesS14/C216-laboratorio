def _payload(nome="Alimentacao", tipo="despesa"):
    return {"nome": nome, "tipo": tipo}

def test_criar_categoria(client):
    resp = client.post("/api/v1/categorias/", json=_payload())
    assert resp.status_code == 201
    assert resp.json()["nome"] == "Alimentacao"

def test_listar_categorias(client):
    client.post("/api/v1/categorias/", json=_payload("Salario", "receita"))
    client.post("/api/v1/categorias/", json=_payload("Transporte", "despesa"))
    client.post("/api/v1/categorias/", json=_payload("Lazer", "despesa"))
    resp = client.get("/api/v1/categorias/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

def test_buscar_categoria(client):
    criada = client.post("/api/v1/categorias/", json=_payload()).json()
    resp = client.get(f"/api/v1/categorias/{criada['id']}")
    assert resp.status_code == 200

def test_atualizar_categoria(client):
    criada = client.post("/api/v1/categorias/", json=_payload()).json()
    resp = client.put(f"/api/v1/categorias/{criada['id']}", json=_payload("Mercado", "despesa"))
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Mercado"

def test_deletar_categoria(client):
    criada = client.post("/api/v1/categorias/", json=_payload()).json()
    resp = client.delete(f"/api/v1/categorias/{criada['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/v1/categorias/{criada['id']}").status_code == 404
