from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.conta import Conta, ContaCreate
from app.services import conta_service

router = APIRouter(prefix="/api/v1/contas", tags=["Contas"])

@router.get("/", response_model=list[Conta])
def listar(db: Session = Depends(get_db)):
    return conta_service.listar(db)

@router.get("/{conta_id}", response_model=Conta)
def buscar(conta_id: int, db: Session = Depends(get_db)):
    conta = conta_service.buscar_por_id(db, conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta nao encontrada")
    return conta

@router.post("/", response_model=Conta, status_code=201)
def criar(dados: ContaCreate, db: Session = Depends(get_db)):
    return conta_service.criar(db, dados)

@router.put("/{conta_id}", response_model=Conta)
def atualizar(conta_id: int, dados: ContaCreate, db: Session = Depends(get_db)):
    conta = conta_service.atualizar(db, conta_id, dados)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta nao encontrada")
    return conta

@router.delete("/{conta_id}")
def deletar(conta_id: int, db: Session = Depends(get_db)):
    if not conta_service.deletar(db, conta_id):
        raise HTTPException(status_code=404, detail="Conta nao encontrada")
    return {"mensagem": "Conta removida com sucesso"}
