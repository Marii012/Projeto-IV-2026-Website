from app.repositories.base import Tabela, texto, inteiro, livre, ref

tabela = Tabela(
    "ficheiro",
    [
        texto("caminho", "O caminho", 500, obrigatoria=True),
        inteiro("versao", "A versão", 0, 32767, obrigatoria=True, msg="Versão inválida."),
        livre("visivel_cliente"),
        ref("id_encomenda"),
        ref("id_nota"),
        ref("id_enviado_por"),
        ref("id_tipo_ficheiro"),
        ref("id_estado"),
    ],
    so_leitura=("data",),
    ordem="data DESC",
)
