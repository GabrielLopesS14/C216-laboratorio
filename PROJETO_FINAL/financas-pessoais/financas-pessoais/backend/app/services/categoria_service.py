from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate

def listar(db: Session):
    return db.query(Categoria).all()

def buscar_por_id(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def criar(db: Session, dados: CategoriaCreate):
    categoria = Categoria(**dados.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

def atualizar(db: Session, categoria_id: int, dados: CategoriaCreate):
    categoria = buscar_por_id(db, categoria_id)
    if not categoria:
        return None
    for campo, valor in dados.model_dump().items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

def deletar(db: Session, categoria_id: int):
    categoria = buscar_por_id(db, categoria_id)
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True
