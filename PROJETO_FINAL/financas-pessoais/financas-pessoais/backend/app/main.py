from fastapi import FastAPI

from app.database import Base, engine
from app import models  
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header
from app.routes import contas, categorias, transacoes, tags

#Cria as tabelas no banco caso ainda nao existam.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Financas Pessoais",
    description="API REST para controle de financas pessoais (projeto final).",
    version="1.0.0",
)

#Middlewares (interceptam todas as requisicoes)
app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

#Rotas/Endpoints
app.include_router(contas.router)
app.include_router(categorias.router)
app.include_router(transacoes.router)
app.include_router(tags.router)

@app.get("/")
def root():
    return {"mensagem": "API de Financas Pessoais funcionando!"}
