from app.repositories.base import Tabela, texto, inteiro, livre, ref

tabela = Tabela(
    "etapa",
    [
        texto("designacao", "A designação", 100, obrigatoria=True),
        inteiro("ordem", "A ordem", -32768, 32767),
        livre("e_administrativa"),
        livre("limite_cancelamento"),
        ref("id_tipo_trabalho"),
    ],
)
