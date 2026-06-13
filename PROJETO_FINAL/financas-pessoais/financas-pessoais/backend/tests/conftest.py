import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app 

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)

def _get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()

#Substitui a conexao real pela de teste.
app.dependency_overrides[get_db] = _get_db_teste

@pytest.fixture(autouse=True)
def preparar_banco():
    """Cria as tabelas antes de cada teste e apaga depois (isolamento)."""
    Base.metadata.create_all(bind=engine_teste)
    yield
    Base.metadata.drop_all(bind=engine_teste)

@pytest.fixture
def client():
    return TestClient(app)
