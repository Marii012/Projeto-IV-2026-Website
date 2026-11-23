from app.repositories.base import Tabela, texto

tabela = Tabela(
    "estado",
    [texto("descricao", "A descrição", 40, obrigatoria=True)],
    ordem="id",
)
