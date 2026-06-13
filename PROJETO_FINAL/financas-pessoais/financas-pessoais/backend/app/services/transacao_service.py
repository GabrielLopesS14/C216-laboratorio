from sqlalchemy.orm import Session

from app.models.transacao import Transacao
from app.models.tag import Tag
from app.schemas.transacao import TransacaoCreate

def listar(db: Session):
    return db.query(Transacao).all()

def buscar_por_id(db: Session, transacao_id: int):
    return db.query(Transacao).filter(Transacao.id == transacao_id).first()

def _resolver_tags(db: Session, tag_ids: list[int]):
    """Converte uma lista de IDs nos objetos Tag correspondentes."""
    if not tag_ids:
        return []
    return db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

def criar(db: Session, dados: TransacaoCreate):
    dados_dict = dados.model_dump()
    tag_ids = dados_dict.pop("tag_ids", [])

    transacao = Transacao(**dados_dict)
    transacao.tags = _resolver_tags(db, tag_ids)

    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao

def atualizar(db: Session, transacao_id: int, dados: TransacaoCreate):
    transacao = buscar_por_id(db, transacao_id)
    if not transacao:
        return None

    dados_dict = dados.model_dump()
    tag_ids = dados_dict.pop("tag_ids", [])

    for campo, valor in dados_dict.items():
        setattr(transacao, campo, valor)
    transacao.tags = _resolver_tags(db, tag_ids)

    db.commit()
    db.refresh(transacao)
    return transacao

def deletar(db: Session, transacao_id: int):
    transacao = buscar_por_id(db, transacao_id)
    if not transacao:
        return False
    db.delete(transacao)
    db.commit()
    return True
