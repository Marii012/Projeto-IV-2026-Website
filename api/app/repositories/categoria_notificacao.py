from app.repositories.base import Tabela, texto

tabela = Tabela(
    "categoria_notificacao",
    [texto("descricao", "A descrição", 50, obrigatoria=True)],
    ordem="id",
)
