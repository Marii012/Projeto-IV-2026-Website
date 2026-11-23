from app.repositories.base import Tabela, texto, livre, ref

tabela = Tabela(
    "notificacao",
    [
        texto("titulo", "O título", 150, obrigatoria=True),
        livre("descricao"),
        livre("lida"),
        ref("id_utilizador"),
        ref("id_encomenda"),
        ref("id_categoria"),
    ],
    so_leitura=("data",),
    ordem="data DESC",
    # colaboradores e clientes só veem as suas próprias notificações
    restricao={2: ("id_utilizador", "id"), 3: ("id_utilizador", "id")},
)
