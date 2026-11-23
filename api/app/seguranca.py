"""Passwords e tokens JWT.

As passwords usam o formato do Django (pbkdf2_sha256$iterações$salt$hash),
por isso as contas que já existem na base de dados continuam a funcionar.
"""
import base64
import hashlib
import hmac
import secrets
import string
from datetime import datetime, timedelta, timezone

import jwt

from app.config import JWT_ALGORITMO, JWT_EXPIRA_MINUTOS, JWT_SECRET

ITERACOES = 870_000
_ALFABETO = string.ascii_letters + string.digits


def gerar_hash(password):
    """Devolve o hash de uma password. Com None cria uma conta sem password utilizável."""
    if password is None:
        return "!" + "".join(secrets.choice(_ALFABETO) for _ in range(40))
    salt = "".join(secrets.choice(_ALFABETO) for _ in range(22))
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERACOES)
    return f"pbkdf2_sha256${ITERACOES}${salt}${base64.b64encode(dk).decode()}"


def verificar_password(password: str, hash_guardado) -> bool:
    if not hash_guardado or hash_guardado.startswith("!"):
        return False
    try:
        algoritmo, iteracoes, salt, esperado = hash_guardado.split("$", 3)
        if algoritmo != "pbkdf2_sha256":
            return False
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), int(iteracoes)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(base64.b64encode(dk).decode(), esperado)


def criar_token(id_utilizador: int, tipo: int, id_cliente=None) -> str:
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(id_utilizador),
        "tipo": tipo,
        "cid": id_cliente,
        "iat": agora,
        "exp": agora + timedelta(minutes=JWT_EXPIRA_MINUTOS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITMO)


def ler_token(token: str) -> dict:
    """Valida o token e devolve o payload (levanta jwt.PyJWTError se inválido/expirado)."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO])
