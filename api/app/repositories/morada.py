from app.repositories.base import Tabela, texto, ref

tabela = Tabela(
    "morada",
    [
        texto("nome_clinica", "O nome da clínica", 120, obrigatoria=True),
        texto("morada", "A morada", 255, obrigatoria=True),
        ref("id_cliente"),
    ],
)
