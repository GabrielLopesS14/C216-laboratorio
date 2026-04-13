from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()

#Simulando o banco de dados
alunos = {}
contadores_curso = {}

def gerar_matricula(curso: str):
    """Gera matrícula sequencial baseada no curso"""
    curso = curso.upper()
    if curso not in contadores_curso:
        contadores_curso[curso] = 1
    else:
        contadores_curso[curso] += 1
    return f"{curso}{contadores_curso[curso]}"

#Modelos de Dados
class Aluno(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoResponse(Aluno):
    matricula: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

#Middleware de Log
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response

#Rotas
@app.get("/")
async def root():
    return {"message": "Sistema de Gerenciamento de Alunos - API FastAPI"}

#POST
@app.post("/api/v1/alunos", response_model=AlunoResponse, status_code=201)
async def criar_aluno(aluno: Aluno):
    cursos_validos = ["GES", "GEC", "GET", "GEA", "GEP"]
    curso_upper = aluno.curso.upper()
    
    if curso_upper not in cursos_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Curso inválido. Escolha entre: {', '.join(cursos_validos)}"
        )
    
    matricula = gerar_matricula(curso_upper)
    novo_aluno = AlunoResponse(
        nome=aluno.nome,
        email=aluno.email,
        curso=curso_upper,
        matricula=matricula
    )
    
    alunos[matricula] = novo_aluno
    return novo_aluno

#GET
@app.get("/api/v1/alunos", response_model=List[AlunoResponse])
async def listar_alunos():
    return list(alunos.values())

#GET
@app.get("/api/v1/alunos/{matricula}", response_model=AlunoResponse)
async def obter_aluno(matricula: str):
    matricula_upper = matricula.upper()
    if matricula_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return alunos[matricula_upper]

#PUT
@app.put("/api/v1/alunos/{matricula}", response_model=AlunoResponse)
async def atualizar_aluno(matricula: str, dados: Aluno):
    matricula_upper = matricula.upper()
    if matricula_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    aluno_atualizado = AlunoResponse(
        nome=dados.nome,
        email=dados.email,
        curso=dados.curso.upper(),
        matricula=matricula_upper
    )
    alunos[matricula_upper] = aluno_atualizado
    return aluno_atualizado

#PATCH
@app.patch("/api/v1/alunos/{matricula}", response_model=AlunoResponse)
async def modificar_aluno(matricula: str, dados_parciais: AlunoUpdate):
    matricula_upper = matricula.upper()
    if matricula_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    aluno_data = alunos[matricula_upper].dict()
    update_data = dados_parciais.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        aluno_data[key] = value
        
    aluno_final = AlunoResponse(**aluno_data)
    alunos[matricula_upper] = aluno_final
    return aluno_final

#DELETE
@app.delete("/api/v1/alunos/{matricula}")
async def deletar_aluno(matricula: str):
    matricula_upper = matricula.upper()
    if matricula_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    del alunos[matricula_upper]
    return {"message": f"Aluno com matrícula {matricula_upper} deletado com sucesso"}