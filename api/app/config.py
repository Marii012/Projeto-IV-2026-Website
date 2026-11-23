"""Configuração da API (lida de variáveis de ambiente / ficheiro .env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _obrigatoria(nome: str) -> str:
    valor = os.environ.get(nome)
    if not valor:
        raise RuntimeError(
            f"Variável de ambiente '{nome}' em falta. "
            "Copia api/.env.example para api/.env e preenche-a."
        )
    return valor


DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", ""),
    "user": os.environ.get("DB_USER", ""),
    "password": os.environ.get("DB_PASSWORD", ""),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
}

JWT_SECRET = os.environ.get(
    "JWT_SECRET", "dev-only-change-this-secret-key-0123456789abcdef"
)
JWT_ALGORITMO = "HS256"
JWT_EXPIRA_MINUTOS = int(os.environ.get("JWT_EXPIRA_MINUTOS", "480"))

# Ids fixos usados pela lógica de negócio (tabelas estado / tipo_utilizador).
TIPO_ADMIN = 1
TIPO_COLABORADOR = 2
TIPO_CLIENTE = 3

ESTADO_PENDENTE = 1   # conta criada pelo registo público, a aguardar aprovação
ESTADO_ATIVO = 12     # conta criada/aprovada por um administrador
