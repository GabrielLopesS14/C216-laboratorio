from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema de Gerenciamento" in response.json()["message"]

def test_criar_aluno_sucesso():
    """CORREÇÃO: Alterado curso para GES para coincidir com a matrícula esperada GES1"""
    payload = {
        "nome": "Gabriel Lopes Silva",
        "email": "gabriel@inatel.br",
        "curso": "GES"
    }
    response = client.post("/api/v1/alunos", json=payload)
    assert response.status_code == 201
    assert response.json()["matricula"] == "GES1"

def test_criar_aluno_curso_invalido():
    payload = {
        "nome": "Aluno Teste",
        "email": "teste@email.com",
        "curso": "DIREITO"
    }
    response = client.post("/api/v1/alunos", json=payload)
    assert response.status_code == 400

def test_obter_aluno_por_matricula():
    response = client.get("/api/v1/alunos/GES1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Gabriel Lopes Silva"

def test_atualizar_aluno():
    payload = {
        "nome": "Gabriel Silva",
        "email": "gabriel.novo@inatel.br",
        "curso": "GES"
    }
    response = client.put("/api/v1/alunos/GES1", json=payload)
    assert response.status_code == 200
    assert response.json()["nome"] == "Gabriel Silva"

def test_deletar_aluno():
    response = client.delete("/api/v1/alunos/GES1")
    assert response.status_code == 200
    assert "deletado com sucesso" in response.json()["message"]

def test_aluno_nao_encontrado():
    response = client.get("/api/v1/alunos/MATRICULA999")
    assert response.status_code == 404