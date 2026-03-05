from fastapi import FastAPI

app = FastAPI()

from routes.auth_routes import auth_routes
from routes.order_routes import order_routes

app.include_router(auth_routes)
app.include_router(order_routes)

# para rodar o nosso codigo, executrar no terminal: uvicorn main:app --reload