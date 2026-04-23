from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import time

app = FastAPI()

alunos = {}
contadores_curso = {"GES": 0, "GEC": 0}

class Aluno(BaseModel):
    nome: str
    email: EmailStr
    curso: str

class AlunoResponse(Aluno):
    matricula: int
    id: str

class AlunoPatch(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response

#Endpoints

@app.post("/api/v1/alunos/", response_model=AlunoResponse, status_code=201)
async def cadastrar_aluno(aluno: Aluno):
    curso_upper = aluno.curso.upper()
    if curso_upper not in ["GES", "GEC"]:
        raise HTTPException(status_code=400, detail="Cursos permitidos: GES ou GEC")
    
    #Incrementa contador e garante que ID nunca seja reutilizado
    contadores_curso[curso_upper] += 1
    num_matricula = contadores_curso[curso_upper]
    aluno_id = f"{curso_upper}{num_matricula}"
    
    novo_aluno = AlunoResponse(
        nome=aluno.nome,
        email=aluno.email,
        curso=curso_upper,
        matricula=num_matricula,
        id=aluno_id
    )
    
    alunos[aluno_id] = novo_aluno
    return novo_aluno

@app.get("/api/v1/alunos/", response_model=List[AlunoResponse])
async def listar_alunos():
    return list(alunos.values())

@app.get("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
async def buscar_aluno(aluno_id: str):
    id_upper = aluno_id.upper()
    if id_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return alunos[id_upper]

@app.patch("/api/v1/alunos/{aluno_id}", response_model=AlunoResponse)
async def atualizar_aluno(aluno_id: str, dados: AlunoPatch):
    id_upper = aluno_id.upper()
    if id_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    aluno_atual = alunos[id_upper].dict()
    update_data = dados.dict(exclude_unset=True)
    
    #Se mudar o curso, apenas atualiza o texto, o ID e Matrícula permanecem os mesmos da criação
    aluno_atual.update(update_data)
    
    aluno_final = AlunoResponse(**aluno_atual)
    alunos[id_upper] = aluno_final
    return aluno_final

@app.delete("/api/v1/alunos/{aluno_id}")
async def remover_aluno(aluno_id: str):
    id_upper = aluno_id.upper()
    if id_upper not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    del alunos[id_upper]
    return {"message": f"Aluno {id_upper} removido com sucesso"}

@app.delete("/api/v1/alunos/")
async def resetar_lista():
    alunos.clear()
    return {"message": "Lista de alunos resetada com sucesso"}