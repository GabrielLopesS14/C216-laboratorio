from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nome: str
    tipo: str            # 'receita' ou 'despesa'

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    model_config = {"from_attributes": True}
