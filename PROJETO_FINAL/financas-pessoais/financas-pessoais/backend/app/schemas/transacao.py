from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.conta import Conta
from app.schemas.categoria import Categoria
from app.schemas.tag import Tag

class TransacaoBase(BaseModel):
    descricao: str
    valor: Decimal
    data: date
    tipo: str            #receita ou despesa
    conta_id: int
    categoria_id: int

class TransacaoCreate(TransacaoBase):
    """Na criacao, recebemos apenas os IDs das tags a associar."""
    tag_ids: list[int] = []

class Transacao(TransacaoBase):
    """Na resposta, devolvemos os objetos completos (conta, categoria, tags)."""
    id: int
    conta: Conta | None = None
    categoria: Categoria | None = None
    tags: list[Tag] = []

    model_config = {"from_attributes": True}
