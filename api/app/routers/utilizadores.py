from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app import servicos
from app.config import TIPO_ADMIN, TIPO_CLIENTE, TIPO_COLABORADOR
from app.db import transacao
from app.dependencias import requer
from app.repositories import utilizador
from app.schemas import UtilizadorAdminIn, UtilizadorIn

router = APIRouter(prefix="/utilizadores", tags=["Utilizadores"])
admin = Depends(requer(TIPO_ADMIN))


@router.get("", summary="Listar utilizadores (sem passwords)")
def listar(_=admin):
    with transacao() as cur:
        return utilizador.listar(cur)


@router.get("/painel", summary="Painel do administrador: listagem por tipo + totais")
def painel(tipo: str = "clientes", pesquisa: str = "", _=admin):
    tipo = "colaboradores" if tipo == "colaboradores" else "clientes"
    id_tipo = TIPO_COLABORADOR if tipo == "colaboradores" else TIPO_CLIENTE
    with transacao() as cur:
        return {
            "tipo": tipo,
            "total_clientes": utilizador.contar_por_tipo(cur, TIPO_CLIENTE),
            "total_colaboradores": utilizador.contar_por_tipo(cur, TIPO_COLABORADOR),
            "utilizadores": utilizador.listar_por_tipo(cur, id_tipo, pesquisa.strip()),
        }


@router.post("/admin", status_code=201,
             summary="Criar cliente ou colaborador (conta ativa, sem password)")
def criar_pelo_admin(dados: UtilizadorAdminIn, _=admin):
    with transacao() as cur:
        id_utilizador = servicos.criar_utilizador_admin(cur, dados)
    return {"id": id_utilizador}


@router.get("/{id}")
def obter(id: int, _=admin):
    with transacao() as cur:
        u = utilizador.obter(cur, id)
    if u is None:
        raise HTTPException(404, "Utilizador não encontrado.")
    return u


@router.post("", status_code=201)
def criar(d: UtilizadorIn, _=admin):
    with transacao() as cur:
        novo = utilizador.inserir(cur, d.nome, d.email, d.password, d.cargo,
                                  d.id_tipo_utilizador, d.id_estado)
        return utilizador.obter(cur, novo)


@router.put("/{id}", summary="Atualizar (a password só muda se for enviada)")
def atualizar(id: int, d: UtilizadorIn, _=admin):
    with transacao() as cur:
        if not utilizador.atualizar(cur, id, d.nome, d.email, d.password, d.cargo,
                                    d.id_tipo_utilizador, d.id_estado):
            raise HTTPException(404, "Utilizador não encontrado.")
        return utilizador.obter(cur, id)


@router.delete("/{id}", status_code=204)
def eliminar(id: int, _=admin):
    with transacao() as cur:
        if not utilizador.eliminar(cur, id):
            raise HTTPException(404, "Utilizador não encontrado.")
