from django.db import connection


def listar_tipos_solicitacao():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_solicitacao
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_tipo_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_solicitacao
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_tipo_solicitacao(descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO tipo_solicitacao (descricao)
            VALUES (%s)
        """, [descricao])


def atualizar_tipo_solicitacao(id, descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE tipo_solicitacao
            SET descricao = %s
            WHERE id = %s
        """, [descricao, id])


def eliminar_tipo_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM tipo_solicitacao
            WHERE id = %s
        """, [id])
