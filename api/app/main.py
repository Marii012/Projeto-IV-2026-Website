"""API do Laboratório (Projeto IV).

Único componente com acesso à base de dados. O site Django consome esta API.
Arranque (a partir da pasta api/):  uvicorn app.main:app --reload --port 8001
Documentação interativa:             http://127.0.0.1:8001/docs
"""
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, HTTPException

from app.db import fechar_pool, transacao
from app.dependencias import UtilizadorAtual, autenticado
from app.erros import registar_handlers
from app.routers import auth, utilizadores
from app.routers.tabelas import todos_os_routers

@asynccontextmanager
async def _ciclo_de_vida(_: FastAPI):
    yield
    fechar_pool()


app = FastAPI(title="API Laboratório - Projeto IV", version="1.0.0",
              lifespan=_ciclo_de_vida)
registar_handlers(app)

app.include_router(auth.router)
app.include_router(utilizadores.router)

# Marcar notificação como lida (o dono da notificação, qualquer tipo de utilizador).
_notif = APIRouter(prefix="/notificacoes", tags=["Notificações"])


@_notif.patch("/{id}/lida", summary="Marcar a minha notificação como lida")
def marcar_lida(id: int, u: UtilizadorAtual = Depends(autenticado)):
    with transacao() as cur:
        cur.execute(
            "UPDATE notificacao SET lida = TRUE WHERE id = %s AND id_utilizador = %s "
            "RETURNING id", [id, u.id])
        if cur.fetchone() is None:
            raise HTTPException(404, "Notificação não encontrada.")
    return {"id": id, "lida": True}


app.include_router(_notif)
for r in todos_os_routers():
    app.include_router(r)


@app.get("/saude", tags=["Sistema"], summary="Verifica se a API e a BD respondem")
def saude():
    with transacao() as cur:
        cur.execute("SELECT 1 AS ok")
        cur.fetchone()
    return {"estado": "ok"}

