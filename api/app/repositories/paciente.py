from app.repositories.base import Tabela, texto

tabela = Tabela(
    "paciente",
    [
        texto("identificador", "O identificador", 60, obrigatoria=True),
        texto("sexo", "O sexo", 1, obrigatoria=True, msg="O sexo só pode ter 1 carácter."),
    ],
)
