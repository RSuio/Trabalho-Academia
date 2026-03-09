from fastapi import APIRouter, Depends, HTTPException
from database.models import Usuario
from routes.dependeces import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_routes = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"asudihiuashd2q18737812yuisad{id_usuario}"
    return token

@auth_routes.get("/")
async def home():
    return {"mensagem": "voce acessou a rota padrão de autenticação.", "autenticado":False}

@auth_routes.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code = 400, detail="E-mail do usuário já cadastrado")
        # Já existe um usuario com esse email
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada, usuario_schema.admin, usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem":f"Usuário cadastrado com sucesso {usuario_schema.email}."}
    
# login -> email e senha -> token JWT (Json Web Toekn) hiudsahiushd12y3812dagsdyugasdy

@auth_routes.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code = 400, detail="Esse usuario não existe")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "acess_token": acess_token,
            "token_type": "Bearer"
            }
    
    
    
