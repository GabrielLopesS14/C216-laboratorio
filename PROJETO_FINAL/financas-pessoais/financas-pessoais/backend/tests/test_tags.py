def test_criar_tag(client):
    resp = client.post("/api/v1/tags/", json={"nome": "viagem"})
    assert resp.status_code == 201
    assert resp.json()["nome"] == "viagem"

def test_listar_tags(client):
    client.post("/api/v1/tags/", json={"nome": "trabalho"})
    client.post("/api/v1/tags/", json={"nome": "casa"})
    client.post("/api/v1/tags/", json={"nome": "lazer"})
    resp = client.get("/api/v1/tags/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

def test_buscar_tag(client):
    criada = client.post("/api/v1/tags/", json={"nome": "fixo"}).json()
    resp = client.get(f"/api/v1/tags/{criada['id']}")
    assert resp.status_code == 200

def test_atualizar_tag(client):
    criada = client.post("/api/v1/tags/", json={"nome": "antigo"}).json()
    resp = client.put(f"/api/v1/tags/{criada['id']}", json={"nome": "novo"})
    assert resp.status_code == 200
    assert resp.json()["nome"] == "novo"

def test_deletar_tag(client):
    criada = client.post("/api/v1/tags/", json={"nome": "remover"}).json()
    resp = client.delete(f"/api/v1/tags/{criada['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/v1/tags/{criada['id']}").status_code == 404
