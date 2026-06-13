from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.categoria import Categoria, CategoriaCreate
from app.services import categoria_service

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorias"])

@router.get("/", response_model=list[Categoria])
def listar(db: Session = Depends(get_db)):
    return categoria_service.listar(db)

@router.get("/{categoria_id}", response_model=Categoria)
def buscar(categoria_id: int, db: Session = Depends(get_db)):
    categoria = categoria_service.buscar_por_id(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria nao encontrada")
    return categoria

@router.post("/", response_model=Categoria, status_code=201)
def criar(dados: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_service.criar(db, dados)

@router.put("/{categoria_id}", response_model=Categoria)
def atualizar(categoria_id: int, dados: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = categoria_service.atualizar(db, categoria_id, dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria nao encontrada")
    return categoria

@router.delete("/{categoria_id}")
def deletar(categoria_id: int, db: Session = Depends(get_db)):
    if not categoria_service.deletar(db, categoria_id):
        raise HTTPException(status_code=404, detail="Categoria nao encontrada")
    return {"mensagem": "Categoria removida com sucesso"}
