"""Converte erros da base de dados em respostas HTTP com mensagens claras."""
import psycopg2
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg2 import errors

from app.repositories.base import ErroValidacao

_MENSAGENS_UNICAS = {
    "utilizador_email_key": "O e-mail introduzido já está associado a outra conta.",
    "cliente_nif_key": "O NIF introduzido já está associado a outro cliente.",
    "cliente_id_utilizador_key": "Este utilizador já tem um registo de cliente.",
}


def _resp(status, detalhe):
    return JSONResponse(status_code=status, content={"detail": detalhe})


def registar_handlers(app: FastAPI):
    @app.exception_handler(ErroValidacao)
    async def _validacao(_: Request, e: ErroValidacao):
        return _resp(400, str(e))

    @app.exception_handler(RequestValidationError)
    async def _pedido_invalido(_: Request, e: RequestValidationError):
        campo = ".".join(str(p) for p in e.errors()[0]["loc"] if p != "body") or "pedido"
        return _resp(422, f"Valor inválido ou em falta no campo '{campo}'.")

    @app.exception_handler(errors.UniqueViolation)
    async def _unico(_: Request, e):
        nome = e.diag.constraint_name or ""
        return _resp(409, _MENSAGENS_UNICAS.get(
            nome, "Já existe um registo com estes dados."))

    @app.exception_handler(errors.ForeignKeyViolation)
    async def _fk(_: Request, e):
        return _resp(409, "Referência inválida ou registo em uso por outros dados.")

    @app.exception_handler(errors.NotNullViolation)
    async def _nulo(_: Request, e):
        return _resp(400, f"O campo '{e.diag.column_name}' é obrigatório.")

    @app.exception_handler(errors.CheckViolation)
    async def _check(_: Request, e):
        return _resp(400, "Os dados não cumprem as regras definidas para este registo.")

    @app.exception_handler(psycopg2.DataError)
    async def _dados(_: Request, e):
        return _resp(400, "Formato ou tamanho de dados inválido.")

    @app.exception_handler(psycopg2.OperationalError)
    async def _indisponivel(_: Request, e):
        print("ERRO DE LIGAÇÃO À BD:", repr(e))
        return _resp(503, "Base de dados indisponível. Tenta novamente mais tarde.")

    @app.exception_handler(psycopg2.Error)
    async def _outro(_: Request, e):
        print("ERRO DE BD:", repr(e))
        return _resp(500, "Erro interno ao aceder aos dados.")
