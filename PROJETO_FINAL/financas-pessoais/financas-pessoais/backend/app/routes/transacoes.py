from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transacao import Transacao, TransacaoCreate
from app.services import transacao_service

router = APIRouter(prefix="/api/v1/transacoes", tags=["Transacoes"])

@router.get("/", response_model=list[Transacao])
def listar(db: Session = Depends(get_db)):
    return transacao_service.listar(db)

@router.get("/{transacao_id}", response_model=Transacao)
def buscar(transacao_id: int, db: Session = Depends(get_db)):
    transacao = transacao_service.buscar_por_id(db, transacao_id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    return transacao

@router.post("/", response_model=Transacao, status_code=201)
def criar(dados: TransacaoCreate, db: Session = Depends(get_db)):
    return transacao_service.criar(db, dados)

@router.put("/{transacao_id}", response_model=Transacao)
def atualizar(transacao_id: int, dados: TransacaoCreate, db: Session = Depends(get_db)):
    transacao = transacao_service.atualizar(db, transacao_id, dados)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    return transacao

@router.delete("/{transacao_id}")
def deletar(transacao_id: int, db: Session = Depends(get_db)):
    if not transacao_service.deletar(db, transacao_id):
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    return {"mensagem": "Transacao removida com sucesso"}
