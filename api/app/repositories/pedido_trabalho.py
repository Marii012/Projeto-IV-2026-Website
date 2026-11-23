from app.repositories.base import Tabela, texto, livre, ref

tabela = Tabela(
    "pedido_trabalho",
    [
        livre("e_digital"),
        livre("material_da_clinica"),
        texto("material_desc", "A descrição do material", 255),
        texto("material_qtd", "A quantidade de material", 50),
        livre("material_obs"),
        texto("cor", "A cor", 50),
        texto("dentes", "A informação dos dentes", 100),
        livre("data_proxima_consulta"),
        ref("id_encomenda"),
        ref("id_tipo_trabalho"),
        ref("id_estado"),
        ref("id_material"),
    ],
)
