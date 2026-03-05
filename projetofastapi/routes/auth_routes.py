from fastapi import APIRouter

auth_routes = APIRouter(prefix="/auth", tags=["auth"])

@auth_routes.get("/")
async def autenticar():
    return {"mensagem": "voce acessou a rota padrão de autenticação.", "autenticado":False}
