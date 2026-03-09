from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from routes.dependeces import pegar_sessao
from schemas import PedidoSchema
from database.models import Pedido


order_routes = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_routes.get("/")
async def pedidos():
    return {"mensagem": "voce acessou a rota de pedidos."}

@order_routes.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido {novo_pedido.id}"}    
    