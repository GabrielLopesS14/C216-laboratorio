from fastapi.testclient import TestClient
import pytest
import time
from app.main import app

client = TestClient(app)

def test_crud_completo_postgresql():
    #Resetar a lista para começar o teste limpo
    client.delete("/api/v1/alunos/")

    #Adição de 3 alunos por curso (GES e GEC)
    cursos = ["GES", "GEC"]
    for curso in cursos:
        for i in range(1, 4):
            payload = {
                "nome": f"Aluno {curso} {i}",
                "email": f"aluno_{curso.lower()}_{i}@inatel.br",
                "curso": curso
            }
            response = client.post("/api/v1/alunos/", json=payload)
            assert response.status_code == 201
            #Verifica se o ID foi gerado corretamente
            assert response.json()["id"] == f"{curso}{i}"

    #Listagem de alunos (deve haver 6)
    response_list = client.get("/api/v1/alunos/")
    assert response_list.status_code == 200
    assert len(response_list.json()) == 6

    #Busca por ID
    response_id = client.get("/api/v1/alunos/GES1")
    assert response_id.status_code == 200
    assert response_id.json()["nome"] == "Aluno GES 1"

    #Atualização de dados (PATCH)
    patch_payload = {
        "nome": "Gabriel Lopes Silva",
        "email": "gabriel@inatel.br",
        "curso": "GES"
    }
    response_patch = client.patch("/api/v1/alunos/GES1", json=patch_payload)
    assert response_patch.status_code == 200
    assert response_patch.json()["nome"] == "Gabriel Lopes Silva"

    #Remoção de aluno
    response_del = client.delete("/api/v1/alunos/GES1")
    assert response_del.status_code == 200

    #Validar que o ID não é reutilizado
    novo_payload = {
        "nome": "Novo Aluno GES",
        "email": "novo@inatel.br",
        "curso": "GES"
    }
    response_novo = client.post("/api/v1/alunos/", json=novo_payload)
    assert response_novo.json()["id"] == "GES4"