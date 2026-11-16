from django.db import connection


def listar_motivos_solicitacao():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, id_tipo_solicitacao
            FROM motivo_solicitacao
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_motivo_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, id_tipo_solicitacao
            FROM motivo_solicitacao
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_motivo_solicitacao(descricao, id_tipo_solicitacao):
    if len(descricao) > 80:
        raise ValueError("A descrição não pode ultrapassar 80 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO motivo_solicitacao (descricao, id_tipo_solicitacao)
            VALUES (%s, %s)
        """, [descricao, id_tipo_solicitacao])


def atualizar_motivo_solicitacao(id, descricao, id_tipo_solicitacao):
    if len(descricao) > 80:
        raise ValueError("A descrição não pode ultrapassar 80 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE motivo_solicitacao
            SET descricao = %s,
                id_tipo_solicitacao = %s
            WHERE id = %s
        """, [descricao, id_tipo_solicitacao, id])


def eliminar_motivo_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM motivo_solicitacao
            WHERE id = %s
        """, [id])
