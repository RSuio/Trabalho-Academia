from fastapi import APIRouter, Depends, HTTPException
from database.models import Usuario
from routes.dependeces import pegar_sessao
from main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_routes = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario: int):
    # coloquei agora o token com 24 horas de duração.
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(hours=24)
    
    payload = {
        "sub": str(id_usuario),
        "exp": tempo_expiracao
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str, session: Session):
    try:
        # Decodifica o token. Se o tempo exp já passou, ele lança JWTError
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: str = payload.get("sub")
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
        usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado.")
        return usuario
    except JWTError:
        # Se o token expirou ou é incorreto, vem pra ca
        raise HTTPException(status_code=401, detail="Sessão expirada. Por favor, faça login novamente.")


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code = 401, detail="Esse usuario não existe ou credenciais invalidas.")
    # apenas um token com validade de 24h
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400 
    }
