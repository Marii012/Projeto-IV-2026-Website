from app.repositories.base import Tabela, texto, livre, ref

tabela = Tabela(
    "cliente",
    [
        texto("nome", "O nome", 120, obrigatoria=True),
        texto("nif", "O NIF", tam_exato=9, obrigatoria=True,
              msg="O NIF deve ter exatamente 9 caracteres."),
        texto("telefone", "O telefone", 20),
        livre("data_aprovacao"),
        ref("id_utilizador"),
    ],
)
