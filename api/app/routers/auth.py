from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import servicos
from app.config import TIPO_CLIENTE
from app.db import transacao
from app.dependencias import UtilizadorAtual, autenticado
from app.repositories import utilizador
from app.schemas import LoginIn, RegistoIn, TokenOut, UtilizadorSessao
from app.seguranca import criar_token, verificar_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def _autenticar(email: str, password: str) -> TokenOut:
    email = email.strip()
    if len(email) > 150:
        raise HTTPException(400, "O email não pode ultrapassar 150 caracteres.")
    with transacao() as cur:
        u = utilizador.obter_por_email_com_hash(cur, email)
        if u is None or not verificar_password(password, u["password_hash"]):
            raise HTTPException(401, "Email ou palavra-passe inválidos.")
        id_cliente = None
        if u["id_tipo_utilizador"] == TIPO_CLIENTE:
            id_cliente = utilizador.obter_id_cliente(cur, u["id"])
    token = criar_token(u["id"], u["id_tipo_utilizador"], id_cliente)
    return TokenOut(
        access_token=token,
        utilizador=UtilizadorSessao(
            id=u["id"], nome=u["nome"], email=u["email"],
            id_tipo_utilizador=u["id_tipo_utilizador"], id_cliente=id_cliente),
    )


@router.post("/login", response_model=TokenOut, summary="Login (JSON)")
def login(dados: LoginIn):
    return _autenticar(dados.email, dados.password)


@router.post("/token", response_model=TokenOut, include_in_schema=True,
             summary="Login por formulário (botão Authorize do /docs)")
def token(form: OAuth2PasswordRequestForm = Depends()):
    return _autenticar(form.username, form.password)


@router.post("/registo", status_code=201, summary="Registo público de cliente")
def registo(dados: RegistoIn):
    with transacao() as cur:
        id_utilizador = servicos.registar_cliente(cur, dados)
    return {"id": id_utilizador}


@router.get("/me", response_model=UtilizadorSessao, summary="Utilizador autenticado")
def me(atual: UtilizadorAtual = Depends(autenticado)):
    with transacao() as cur:
        u = utilizador.obter(cur, atual.id)
    if u is None:
        raise HTTPException(401, "Utilizador já não existe.")
    return UtilizadorSessao(
        id=u["id"], nome=u["nome"], email=u["email"],
        id_tipo_utilizador=u["id_tipo_utilizador"], id_cliente=atual.cliente_id)
