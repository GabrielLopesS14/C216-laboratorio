from decimal import Decimal

from pydantic import BaseModel

class ContaBase(BaseModel):
    nome: str
    tipo: str
    saldo_inicial: Decimal = Decimal("0")

class ContaCreate(ContaBase):
    """Dados recebidos para criar/atualizar uma conta."""
    pass

class Conta(ContaBase):
    """Dados retornados pela API (inclui o id gerado)."""
    id: int

    model_config = {"from_attributes": True}
