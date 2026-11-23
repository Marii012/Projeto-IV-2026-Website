from app.repositories.base import Tabela, texto

tabela = Tabela(
    "tipo_utilizador",
    [texto("descricao", "A descrição", 30, obrigatoria=True)],
    ordem="id",
)
