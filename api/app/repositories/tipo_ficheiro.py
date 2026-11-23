from app.repositories.base import Tabela, texto

tabela = Tabela(
    "tipo_ficheiro",
    [texto("descricao", "A descrição", 40, obrigatoria=True)],
    ordem="id",
)
