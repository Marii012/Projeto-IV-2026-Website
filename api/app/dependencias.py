"""Autenticação e autorização (quem és tu, e o que podes fazer)."""
from dataclasses import dataclass
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.seguranca import ler_token

_esquema = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


@dataclass
class UtilizadorAtual:
    id: int
    tipo: int
    cliente_id: Optional[int] = None


def autenticado(token: Optional[str] = Depends(_esquema)) -> UtilizadorAtual:
    if not token:
        raise HTTPException(401, "Não autenticado.", headers={"WWW-Authenticate": "Bearer"})
    try:
        p = ler_token(token)
        return UtilizadorAtual(int(p["sub"]), int(p["tipo"]), p.get("cid"))
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(
            401, "Sessão inválida ou expirada.", headers={"WWW-Authenticate": "Bearer"}
        )


def requer(*tipos: int):
    """Dependência que só deixa passar utilizadores de um dos tipos indicados."""

    def verificar(u: UtilizadorAtual = Depends(autenticado)) -> UtilizadorAtual:
        if u.tipo not in tipos:
            raise HTTPException(403, "Não tens permissão para esta operação.")
        return u

    return verificar
