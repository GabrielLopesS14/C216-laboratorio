from pydantic import BaseModel

class TagBase(BaseModel):
    nome: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    model_config = {"from_attributes": True}
