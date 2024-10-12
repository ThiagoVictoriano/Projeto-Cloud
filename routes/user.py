from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, select
from db.db import get_session
from utils.hash_jwt import ACCESS_TOKEN_EXPIRE_MINUTES, generate_token, get_password_hash, verify_password
from utils.api_externa import consulta_api

router = APIRouter(tags=["User"])

class BaseUser(SQLModel):
    nome: str
    email: str

class User(BaseUser, table=True):  # Tabela de usuários no banco de dados
    id_user: int | None = Field(default=None, primary_key=True)
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

@router.post("/register")
def register(user: User, session: Session = Depends(get_session)):
    # Verificar se o email já está registrado no banco de dados
    statement = select(User).where(User.email == user.email)
    result = session.exec(statement).first()
    if result:
        raise HTTPException(status_code=409, detail="Email já registrado")

    # Criar o novo usuário com a senha criptografada
    hashed_senha = get_password_hash(user.senha)

    # Adicionar o novo usuário ao banco de dados
    new_user = User(nome=user.nome, email=user.email, senha=hashed_senha)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Gerar um token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=generate_token(
            data={"sub": new_user.email}, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

    return {"jwt": token.access_token}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Buscar o usuário pelo email (username)
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email não registrado")

    # Verificar a senha
    if not verify_password(form_data.password, user.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    # Gerar um token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=generate_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

    return {"jwt": token.access_token}

@router.get("/consultar")
def consulta(token: Annotated[str, Depends(oauth2_scheme)]):
    data = consulta_api()

    return {
        "data": data
    }