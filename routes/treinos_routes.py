from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from routes.dependeces import pegar_sessao
from routes.auth_routes import verificar_token
from main import oauth2_schema

treinos_routes = APIRouter(prefix="/treinos", tags=["treinos"])

@treinos_routes.get("/meu-treino")
async def ver_meu_treino(usuario_autenticado = Depends(verificar_token)):
    return {
        "usuario": usuario_autenticado.nome,
        "objetivo": "Hipertrofia",
        "treino": [
            {"exercicio": "Supino Reto", "series": 4, "reps": 10},
            {"exercicio": "Crucifixo", "series": 3, "reps": 12},
            {"exercicio": "Tríceps Corda", "series": 4, "reps": 15}
        ],
        "status": "Sessão válida por 24h"
    }