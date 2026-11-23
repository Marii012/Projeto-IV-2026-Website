from app.repositories.base import Tabela, livre, ref

tabela = Tabela(
    "execucao_etapa",
    [
        livre("data_inicio"),
        livre("data_fim"),
        ref("id_pedido_trabalho"),
        ref("id_etapa"),
        ref("id_colaborador"),
    ],
)
