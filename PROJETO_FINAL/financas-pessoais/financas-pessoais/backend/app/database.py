import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/financas",
)

#Engine: o ponto central de comunicação com o banco.
engine = create_engine(DATABASE_URL)

#SessionLocal: fábrica de sessões (cada requisição usa a sua).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base: classe que todos os models herdam para virarem tabelas.
Base = declarative_base()


def get_db():
    """Dependência do FastAPI: abre uma sessão e garante o fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
