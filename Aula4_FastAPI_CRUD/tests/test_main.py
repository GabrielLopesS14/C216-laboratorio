from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def test_crud_completo():
    #Reseta a lista inicial
    client.delete("/api/v1/alunos/")

    #Adicão 3 alunos por curso (GES e GEC)
    for i in range(1, 4):
        client.post("/api/v1/alunos/", json={"nome": f"Aluno GES {i}", "email": f"ges{i}@inatel.br", "curso": "GES"})
        client.post("/api/v1/alunos/", json={"nome": f"Aluno GEC {i}", "email": f"gec{i}@inatel.br", "curso": "GEC"})

    #Listagem de alunos
    resp_list = client.get("/api/v1/alunos/")
    assert len(resp_list.json()) == 6

    #Busca por ID
    resp_busca = client.get("/api/v1/alunos/GES1")
    assert resp_busca.status_code == 200
    assert resp_busca.json()["nome"] == "Aluno GES 1"

    #Atualização de dados (Patch)
    resp_patch = client.patch("/api/v1/alunos/GEC1", json={"nome": "Gabriel Lopes Silva"})
    assert resp_patch.json()["nome"] == "Gabriel Lopes Silva"

    #Remoção de aluno e verificação de não reutilização de ID
    client.delete("/api/v1/alunos/GES1")
    resp_after_del = client.get("/api/v1/alunos/GES1")
    assert resp_after_del.status_code == 404

    #Criar novo GES para provar que ID GES1 não é reutilizado
    resp_novo = client.post("/api/v1/alunos/", json={"nome": "Novo Aluno", "email": "novo@inatel.br", "curso": "GES"})
    assert resp_novo.json()["id"] == "GES4"