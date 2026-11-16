from django.db import connection


def listar_tipos_utilizador():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_utilizador
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_tipo_utilizador(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_utilizador
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_tipo_utilizador(descricao):
    if len(descricao) > 30:
        raise ValueError("A descrição não pode ultrapassar 30 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO tipo_utilizador (descricao)
            VALUES (%s)
        """, [descricao])


def atualizar_tipo_utilizador(id, descricao):
    if len(descricao) > 30:
        raise ValueError("A descrição não pode ultrapassar 30 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE tipo_utilizador
            SET descricao = %s
            WHERE id = %s
        """, [descricao, id])


def eliminar_tipo_utilizador(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM tipo_utilizador
            WHERE id = %s
        """, [id])
