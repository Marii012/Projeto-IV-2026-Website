from django.db import connection


def listar_encomendas():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, cliente_nome_avulso, morada_avulsa,
                   medico_nome, paciente_idade, observacoes_cliente,
                   motivo_standby, data_criacao, data_aceitacao,
                   prazo_dias_uteis, data_limite, data_finalizacao,
                   id_cliente, id_paciente, id_criado_por,
                   id_aceite_por, id_estado, id_encomenda_origem
            FROM encomenda
            ORDER BY data_criacao DESC
        """)
        return cursor.fetchall()


def obter_encomenda(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, cliente_nome_avulso, morada_avulsa,
                   medico_nome, paciente_idade, observacoes_cliente,
                   motivo_standby, data_criacao, data_aceitacao,
                   prazo_dias_uteis, data_limite, data_finalizacao,
                   id_cliente, id_paciente, id_criado_por,
                   id_aceite_por, id_estado, id_encomenda_origem
            FROM encomenda
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_encomenda(
    cliente_nome_avulso, morada_avulsa, medico_nome,
    paciente_idade, observacoes_cliente, motivo_standby,
    data_aceitacao, prazo_dias_uteis, data_limite,
    data_finalizacao, id_cliente, id_paciente,
    id_criado_por, id_aceite_por, id_estado,
    id_encomenda_origem
):
    if cliente_nome_avulso and len(cliente_nome_avulso) > 120:
        raise ValueError("O nome do cliente não pode ultrapassar 120 caracteres.")

    if morada_avulsa and len(morada_avulsa) > 255:
        raise ValueError("A morada não pode ultrapassar 255 caracteres.")

    if len(medico_nome) > 120:
        raise ValueError("O nome do médico não pode ultrapassar 120 caracteres.")

    if not 0 <= paciente_idade <= 32767:
        raise ValueError("A idade do paciente está fora dos limites permitidos.")

    if prazo_dias_uteis is not None and not 0 <= prazo_dias_uteis <= 32767:
        raise ValueError("O prazo está fora dos limites permitidos.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO encomenda (
                cliente_nome_avulso, morada_avulsa, medico_nome,
                paciente_idade, observacoes_cliente, motivo_standby,
                data_aceitacao, prazo_dias_uteis, data_limite,
                data_finalizacao, id_cliente, id_paciente,
                id_criado_por, id_aceite_por, id_estado,
                id_encomenda_origem
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, [
            cliente_nome_avulso, morada_avulsa, medico_nome,
            paciente_idade, observacoes_cliente, motivo_standby,
            data_aceitacao, prazo_dias_uteis, data_limite,
            data_finalizacao, id_cliente, id_paciente,
            id_criado_por, id_aceite_por, id_estado,
            id_encomenda_origem
        ])


def atualizar_encomenda(
    id, cliente_nome_avulso, morada_avulsa, medico_nome,
    paciente_idade, observacoes_cliente, motivo_standby,
    data_aceitacao, prazo_dias_uteis, data_limite,
    data_finalizacao, id_cliente, id_paciente,
    id_criado_por, id_aceite_por, id_estado,
    id_encomenda_origem
):
    if cliente_nome_avulso and len(cliente_nome_avulso) > 120:
        raise ValueError("O nome do cliente não pode ultrapassar 120 caracteres.")

    if morada_avulsa and len(morada_avulsa) > 255:
        raise ValueError("A morada não pode ultrapassar 255 caracteres.")

    if len(medico_nome) > 120:
        raise ValueError("O nome do médico não pode ultrapassar 120 caracteres.")

    if not 0 <= paciente_idade <= 32767:
        raise ValueError("A idade do paciente está fora dos limites permitidos.")

    if prazo_dias_uteis is not None and not 0 <= prazo_dias_uteis <= 32767:
        raise ValueError("O prazo está fora dos limites permitidos.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE encomenda
            SET cliente_nome_avulso = %s,
                morada_avulsa = %s,
                medico_nome = %s,
                paciente_idade = %s,
                observacoes_cliente = %s,
                motivo_standby = %s,
                data_aceitacao = %s,
                prazo_dias_uteis = %s,
                data_limite = %s,
                data_finalizacao = %s,
                id_cliente = %s,
                id_paciente = %s,
                id_criado_por = %s,
                id_aceite_por = %s,
                id_estado = %s,
                id_encomenda_origem = %s
            WHERE id = %s
        """, [
            cliente_nome_avulso, morada_avulsa, medico_nome,
            paciente_idade, observacoes_cliente, motivo_standby,
            data_aceitacao, prazo_dias_uteis, data_limite,
            data_finalizacao, id_cliente, id_paciente,
            id_criado_por, id_aceite_por, id_estado,
            id_encomenda_origem, id
        ])


def eliminar_encomenda(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM encomenda
            WHERE id = %s
        """, [id])


def criar_encomenda(
    id_criador, id_cliente, cliente_nome_avulso,
    morada_avulsa, medico_nome, paciente_identificador,
    paciente_sexo, paciente_idade, observacoes
):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT fn_criar_encomenda(
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, [
            id_criador, id_cliente, cliente_nome_avulso,
            morada_avulsa, medico_nome, paciente_identificador,
            paciente_sexo, paciente_idade, observacoes
        ])

        resultado = cursor.fetchone()
        return resultado[0]

def recusar_encomenda(id_encomenda, id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT fn_recusar_encomenda(%s, %s)
        """, [id_encomenda, id_utilizador])

def entregar_encomenda(id_encomenda, id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT fn_entregar_encomenda(%s, %s)
        """, [id_encomenda, id_utilizador])