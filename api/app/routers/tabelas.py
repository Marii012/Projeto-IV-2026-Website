"""Regista as rotas de todas as tabelas e define quem pode ler/escrever."""
from app.config import TIPO_ADMIN as ADMIN, TIPO_CLIENTE as CLI, TIPO_COLABORADOR as COL
from app.repositories import (
    categoria_notificacao, cliente, encomenda, estado, etapa, execucao_etapa,
    ficheiro, material, morada, motivo_solicitacao, nota, notificacao, paciente,
    pedido_trabalho, solicitacao, solicitacao_trabalho, tipo_ficheiro,
    tipo_solicitacao, tipo_trabalho, tipo_utilizador,
)
from app.routers.crud import criar_router, criar_router_composto

TODOS = (ADMIN, COL, CLI)
EQUIPA = (ADMIN, COL)
SO_ADMIN = (ADMIN,)

# (tabela, prefixo, tag, quem lê, quem escreve)
_ROTAS = [
    # Tabelas de apoio: toda a gente autenticada lê, só o admin altera.
    (estado.tabela, "/estados", "Estados", TODOS, SO_ADMIN),
    (tipo_utilizador.tabela, "/tipos-utilizador", "Tipos de utilizador", TODOS, SO_ADMIN),
    (tipo_ficheiro.tabela, "/tipos-ficheiro", "Tipos de ficheiro", TODOS, SO_ADMIN),
    (tipo_solicitacao.tabela, "/tipos-solicitacao", "Tipos de solicitação", TODOS, SO_ADMIN),
    (tipo_trabalho.tabela, "/tipos-trabalho", "Tipos de trabalho", TODOS, SO_ADMIN),
    (categoria_notificacao.tabela, "/categorias-notificacao", "Categorias de notificação", TODOS, SO_ADMIN),
    (material.tabela, "/materiais", "Materiais", TODOS, SO_ADMIN),
    (motivo_solicitacao.tabela, "/motivos-solicitacao", "Motivos de solicitação", TODOS, SO_ADMIN),
    (etapa.tabela, "/etapas", "Etapas", EQUIPA, SO_ADMIN),
    # Dados da operação: admin e colaboradores.
    (cliente.tabela, "/clientes", "Clientes", EQUIPA, EQUIPA),
    (morada.tabela, "/moradas", "Moradas", EQUIPA, EQUIPA),
    (paciente.tabela, "/pacientes", "Pacientes", EQUIPA, EQUIPA),
    (pedido_trabalho.tabela, "/pedidos-trabalho", "Pedidos de trabalho", EQUIPA, EQUIPA),
    (execucao_etapa.tabela, "/execucoes-etapa", "Execuções de etapa", EQUIPA, EQUIPA),
    (nota.tabela, "/notas", "Notas", EQUIPA, EQUIPA),
    (ficheiro.tabela, "/ficheiros", "Ficheiros", EQUIPA, EQUIPA),
    (solicitacao.tabela, "/solicitacoes", "Solicitações", EQUIPA, EQUIPA),
    # Clientes veem só as suas encomendas (ver restricao em repositories/encomenda.py).
    (encomenda.tabela, "/encomendas", "Encomendas", TODOS, EQUIPA),
    # Cada utilizador vê só as suas notificações; o admin vê todas.
    (notificacao.tabela, "/notificacoes", "Notificações", TODOS, SO_ADMIN),
]


def todos_os_routers():
    routers = [criar_router(*r) for r in _ROTAS]
    routers.append(criar_router_composto(
        solicitacao_trabalho.tabela, "/solicitacoes-trabalho",
        "Solicitações de trabalho", EQUIPA, EQUIPA))
    return routers
