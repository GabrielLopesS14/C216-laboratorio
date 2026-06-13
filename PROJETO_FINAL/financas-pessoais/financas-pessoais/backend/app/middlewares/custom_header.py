from fastapi import Request

async def add_custom_header(request: Request, call_next):
    """Adiciona um cabecalho customizado em todas as respostas."""
    response = await call_next(request)
    response.headers["X-App-Name"] = "Financas-Pessoais"
    return response
