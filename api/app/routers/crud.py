"""Fábrica de rotas CRUD para as tabelas simples (listar/obter/criar/atualizar/eliminar)."""
from fastapi import APIRouter, Depends, HTTPException

from app.db import transacao
from app.dependencias import UtilizadorAtual, requer


def _filtro(tabela, u: UtilizadorAtual):
    """Restringe as linhas visíveis (ex.: um cliente só vê as suas encomendas)."""
    regra = tabela.restricao.get(u.tipo)
    if not regra:
        return None
    coluna, chave = regra
    valor = getattr(u, chave)
    if valor is None:
        raise HTTPException(403, "Não tens permissão para aceder a estes dados.")
    return (coluna, valor)


def _nao_encontrado():
    return HTTPException(404, "Registo não encontrado.")


def criar_router(tabela, prefixo, tag, ler, escrever):
    router = APIRouter(prefix=prefixo, tags=[tag])
    Modelo = tabela.modelo()
    ModeloAtualizar = tabela.modelo(parcial=True)
    pode_ler = Depends(requer(*ler))
    pode_escrever = Depends(requer(*escrever))

    @router.get("", summary=f"Listar {tag.lower()}")
    def listar(u: UtilizadorAtual = pode_ler):
        with transacao() as cur:
            return tabela.listar(cur, _filtro(tabela, u))

    @router.get("/{id}", summary=f"Obter {tag.lower()} por id")
    def obter(id: int, u: UtilizadorAtual = pode_ler):
        with transacao() as cur:
            linha = tabela.obter(cur, [id], _filtro(tabela, u))
        if linha is None:
            raise _nao_encontrado()
        return linha

    @router.post("", status_code=201, summary=f"Criar {tag.lower()}")
    def criar(dados: Modelo, u: UtilizadorAtual = pode_escrever):
        with transacao() as cur:
            return tabela.inserir(cur, dados.model_dump(exclude_unset=True))

    @router.patch("/{id}", summary=f"Atualizar {tag.lower()} (só os campos enviados)")
    def atualizar(id: int, dados: ModeloAtualizar, u: UtilizadorAtual = pode_escrever):
        with transacao() as cur:
            linha = tabela.atualizar(
                cur, [id], dados.model_dump(exclude_unset=True), _filtro(tabela, u))
        if linha is None:
            raise _nao_encontrado()
        return linha

    @router.delete("/{id}", status_code=204, summary=f"Eliminar {tag.lower()}")
    def eliminar(id: int, u: UtilizadorAtual = pode_escrever):
        with transacao() as cur:
            if not tabela.eliminar(cur, [id], _filtro(tabela, u)):
                raise _nao_encontrado()

    return router


def criar_router_composto(tabela, prefixo, tag, ler, escrever):
    """Tabela de ligação com chave primária composta (sem atualização)."""
    router = APIRouter(prefix=prefixo, tags=[tag])
    Modelo = tabela.modelo()
    pode_ler = Depends(requer(*ler))
    pode_escrever = Depends(requer(*escrever))

    @router.get("")
    def listar(u: UtilizadorAtual = pode_ler):
        with transacao() as cur:
            return tabela.listar(cur)

    @router.get("/{id_solicitacao}/{id_pedido_trabalho}")
    def obter(id_solicitacao: int, id_pedido_trabalho: int, u: UtilizadorAtual = pode_ler):
        with transacao() as cur:
            linha = tabela.obter(cur, [id_solicitacao, id_pedido_trabalho])
        if linha is None:
            raise _nao_encontrado()
        return linha

    @router.post("", status_code=201)
    def criar(dados: Modelo, u: UtilizadorAtual = pode_escrever):
        with transacao() as cur:
            return tabela.inserir(cur, dados.model_dump(exclude_unset=True))

    @router.delete("/{id_solicitacao}/{id_pedido_trabalho}", status_code=204)
    def eliminar(id_solicitacao: int, id_pedido_trabalho: int,
                 u: UtilizadorAtual = pode_escrever):
        with transacao() as cur:
            if not tabela.eliminar(cur, [id_solicitacao, id_pedido_trabalho]):
                raise _nao_encontrado()

    return router
