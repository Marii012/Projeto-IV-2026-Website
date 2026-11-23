from app.repositories.base import Tabela, texto, inteiro, livre, ref

tabela = Tabela(
    "encomenda",
    [
        texto("cliente_nome_avulso", "O nome do cliente", 120),
        texto("morada_avulsa", "A morada", 255),
        texto("medico_nome", "O nome do médico", 120, obrigatoria=True),
        inteiro("paciente_idade", "A idade do paciente", 0, 32767, obrigatoria=True),
        livre("observacoes_cliente"),
        livre("motivo_standby"),
        livre("data_aceitacao"),
        inteiro("prazo_dias_uteis", "O prazo", 0, 32767),
        livre("data_limite"),
        livre("data_finalizacao"),
        ref("id_cliente"),
        ref("id_paciente"),
        ref("id_criado_por"),
        ref("id_aceite_por"),
        ref("id_estado"),
        ref("id_encomenda_origem"),
    ],
    so_leitura=("data_criacao",),
    ordem="data_criacao DESC",
    restricao={3: ("id_cliente", "cliente_id")},  # um cliente só vê as suas encomendas
)
