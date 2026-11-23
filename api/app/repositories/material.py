from app.repositories.base import Tabela, texto, livre

tabela = Tabela(
    "material",
    [
        texto("nome", "O nome", 80, obrigatoria=True),
        livre("ativo"),
    ],
)
