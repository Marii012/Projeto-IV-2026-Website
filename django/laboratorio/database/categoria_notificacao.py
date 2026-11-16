from django.db import connection


def listar_categorias():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao
            FROM categoria_notificacao
        """)
        return cursor.fetchall()


def inserir_categoria(descricao):
    if len(descricao) > 50:
        raise ValueError("A descrição não pode ultrapassar 50 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO categoria_notificacao (descricao)
            VALUES (%s)
        """, [descricao])


def atualizar_categoria(id, descricao):
    if len(descricao) > 50:
        raise ValueError("A descrição não pode ultrapassar 50 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE categoria_notificacao
            SET descricao = %s
            WHERE id = %s
        """, [descricao, id])


def eliminar_categoria(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM categoria_notificacao
            WHERE id = %s
        """, [id])
