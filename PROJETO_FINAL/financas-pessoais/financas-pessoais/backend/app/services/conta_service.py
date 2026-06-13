from sqlalchemy.orm import Session

from app.models.conta import Conta
from app.schemas.conta import ContaCreate

def listar(db: Session):
    return db.query(Conta).all()

def buscar_por_id(db: Session, conta_id: int):
    return db.query(Conta).filter(Conta.id == conta_id).first()

def criar(db: Session, dados: ContaCreate):
    conta = Conta(**dados.model_dump())
    db.add(conta)
    db.commit()
    db.refresh(conta)
    return conta

def atualizar(db: Session, conta_id: int, dados: ContaCreate):
    conta = buscar_por_id(db, conta_id)
    if not conta:
        return None
    for campo, valor in dados.model_dump().items():
        setattr(conta, campo, valor)
    db.commit()
    db.refresh(conta)
    return conta

def deletar(db: Session, conta_id: int):
    conta = buscar_por_id(db, conta_id)
    if not conta:
        return False
    db.delete(conta)
    db.commit()
    return True
