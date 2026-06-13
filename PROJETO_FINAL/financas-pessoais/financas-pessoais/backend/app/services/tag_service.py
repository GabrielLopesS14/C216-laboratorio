from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag import TagCreate

def listar(db: Session):
    return db.query(Tag).all()

def buscar_por_id(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def criar(db: Session, dados: TagCreate):
    tag = Tag(**dados.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def atualizar(db: Session, tag_id: int, dados: TagCreate):
    tag = buscar_por_id(db, tag_id)
    if not tag:
        return None
    for campo, valor in dados.model_dump().items():
        setattr(tag, campo, valor)
    db.commit()
    db.refresh(tag)
    return tag

def deletar(db: Session, tag_id: int):
    tag = buscar_por_id(db, tag_id)
    if not tag:
        return False
    db.delete(tag)
    db.commit()
    return True
