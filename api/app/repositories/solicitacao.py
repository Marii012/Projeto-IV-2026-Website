from app.repositories.base import Tabela, livre, ref

tabela = Tabela(
    "solicitacao",
    [
        livre("descricao"),
        livre("data_decisao"),
        ref("id_encomenda"),
        ref("id_solicitante"),
        ref("id_decisor"),
        ref("id_tipo_solicitacao"),
        ref("id_motivo"),
        ref("id_estado"),
    ],
    so_leitura=("data_pedido",),
    ordem="data_pedido DESC",
)
