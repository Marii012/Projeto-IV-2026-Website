from app.repositories.base import Tabela, texto, ref

tabela = Tabela(
    "motivo_solicitacao",
    [
        texto("descricao", "A descrição", 80, obrigatoria=True),
        ref("id_tipo_solicitacao"),
    ],
)
