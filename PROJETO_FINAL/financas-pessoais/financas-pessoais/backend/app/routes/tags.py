from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tag import Tag, TagCreate
from app.services import tag_service

router = APIRouter(prefix="/api/v1/tags", tags=["Tags"])

@router.get("/", response_model=list[Tag])
def listar(db: Session = Depends(get_db)):
    return tag_service.listar(db)


@router.get("/{tag_id}", response_model=Tag)
def buscar(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_service.buscar_por_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag nao encontrada")
    return tag

@router.post("/", response_model=Tag, status_code=201)
def criar(dados: TagCreate, db: Session = Depends(get_db)):
    return tag_service.criar(db, dados)

@router.put("/{tag_id}", response_model=Tag)
def atualizar(tag_id: int, dados: TagCreate, db: Session = Depends(get_db)):
    tag = tag_service.atualizar(db, tag_id, dados)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag nao encontrada")
    return tag

@router.delete("/{tag_id}")
def deletar(tag_id: int, db: Session = Depends(get_db)):
    if not tag_service.deletar(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag nao encontrada")
    return {"mensagem": "Tag removida com sucesso"}
