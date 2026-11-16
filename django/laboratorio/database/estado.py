from django.db import connection


def listar_estados():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM estado
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_estado(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM estado
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_estado(descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO estado (descricao)
            VALUES (%s)
        """, [descricao])


def atualizar_estado(id, descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE estado
            SET descricao = %s
            WHERE id = %s
        """, [descricao, id])


def eliminar_estado(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM estado
            WHERE id = %s
        """, [id])
