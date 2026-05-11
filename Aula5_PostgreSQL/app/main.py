from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel, EmailStr, ConfigDict
import os

#Configuração do Banco
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/items_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AlunoDB(Base):
    __tablename__ = "alunos"
    id = Column(String, primary_key=True)
    nome = Column(String)
    email = Column(String)
    curso = Column(String)
    matricula = Column(Integer)

class ContadorDB(Base):
    __tablename__ = "contadores"
    curso = Column(String, primary_key=True)
    valor = Column(Integer, default=0)

class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    curso: str

class AlunoResponse(AlunoBase):
    id: str
    matricula: int
    model_config = ConfigDict(from_attributes=True) 

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

app = FastAPI()

#ENDPOINTS
@app.post("/api/v1/alunos/", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoBase, db: Session = Depends(get_db)):
    curso_upper = aluno.curso.upper()
    if curso_upper not in ["GES", "GEC"]:
        raise HTTPException(status_code=400, detail="Cursos permitidos: GES, GEC")

    contador = db.query(ContadorDB).filter(ContadorDB.curso == curso_upper).first()
    if not contador:
        contador = ContadorDB(curso=curso_upper, valor=1)
        db.add(contador)
    else:
        contador.valor += 1
    
    db.commit()
    
    aluno_id = f"{curso_upper}{contador.valor}"
    novo_aluno = AlunoDB(**aluno.model_dump(), id=aluno_id, matricula=contador.valor)
    
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

@app.get("/api/v1/alunos/", response_model=list[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(AlunoDB).all()

@app.get("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper()).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.patch("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: str, dados: AlunoBase, db: Session = Depends(get_db)):
    aluno_query = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper())
    aluno = aluno_query.first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    aluno_query.update(dados.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.delete("/api/v1/alunos/{aluno_id}")
def remover_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id.upper()).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(aluno)
    db.commit()
    return {"message": "Removido com sucesso"}

@app.delete("/api/v1/alunos/")
def resetar_lista(db: Session = Depends(get_db)):
    db.query(AlunoDB).delete()
    db.commit()
    return {"message": "Lista resetada"}