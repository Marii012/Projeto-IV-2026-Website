from pydantic import create_model

from app.repositories.base import Tabela


class _SolicitacaoTrabalho(Tabela):
    """Tabela de ligação (chave primária composta, sem atualização)."""

    def modelo(self, parcial=False):
        return create_model(
            "SolicitacaoTrabalhoIn", id_solicitacao=(int, ...), id_pedido_trabalho=(int, ...)
        )


tabela = _SolicitacaoTrabalho(
    "solicitacao_trabalho",
    [],
    pk=("id_solicitacao", "id_pedido_trabalho"),
    ordem="id_solicitacao",
)
