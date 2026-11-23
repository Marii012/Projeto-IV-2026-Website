from app.repositories.base import Tabela, livre, ref

tabela = Tabela(
    "nota",
    [
        livre("texto"),
        livre("visivel_cliente"),
        ref("id_encomenda"),
        ref("id_execucao_etapa"),
        ref("id_autor"),
    ],
    so_leitura=("data",),
    ordem="data DESC",
)
