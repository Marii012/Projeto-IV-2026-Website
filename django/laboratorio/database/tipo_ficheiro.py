from django.db import connection


def listar_tipos_ficheiro():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_ficheiro
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_tipo_ficheiro(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM tipo_ficheiro
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_tipo_ficheiro(descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO tipo_ficheiro (descricao)
            VALUES (%s)
        """, [descricao])


def atualizar_tipo_ficheiro(id, descricao):
    if len(descricao) > 40:
        raise ValueError("A descrição não pode ultrapassar 40 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE tipo_ficheiro
            SET descricao = %s
            WHERE id = %s
        """, [descricao, id])


def eliminar_tipo_ficheiro(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM tipo_ficheiro
            WHERE id = %s
        """, [id])
