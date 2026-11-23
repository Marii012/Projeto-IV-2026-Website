from app.repositories.base import Tabela, texto, livre

tabela = Tabela(
    "tipo_trabalho",
    [
        texto("descricao", "A descrição", 80, obrigatoria=True),
        texto("detalhe", "O detalhe", 255),
        livre("ativo"),
    ],
)
