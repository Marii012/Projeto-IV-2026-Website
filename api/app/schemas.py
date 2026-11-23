from typing import List, Optional

from pydantic import BaseModel


class LoginIn(BaseModel):
    email: str
    password: str


class UtilizadorSessao(BaseModel):
    id: int
    nome: str
    email: str
    id_tipo_utilizador: int
    id_cliente: Optional[int] = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    utilizador: Optional[UtilizadorSessao] = None


class RegistoIn(BaseModel):
    nome: str
    email: str
    telefone: str
    nif: str
    password: str
    confirmar_password: str
    moradas: List[str] = []


class UtilizadorAdminIn(BaseModel):
    tipo: str  # "cliente" | "colaborador"
    nome: str
    email: str
    telefone: Optional[str] = None
    nif: Optional[str] = None
    morada: Optional[str] = None


class UtilizadorIn(BaseModel):
    nome: str
    email: str
    password: Optional[str] = None
    cargo: Optional[str] = None
    id_tipo_utilizador: int
    id_estado: int
