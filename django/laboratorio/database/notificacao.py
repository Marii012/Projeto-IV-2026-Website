from django.db import connection


def listar_notificacoes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, titulo, descricao, lida, data,
                   id_utilizador, id_encomenda, id_categoria
            FROM notificacao
            ORDER BY data DESC
        """)
        return cursor.fetchall()


def obter_notificacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, titulo, descricao, lida, data,
                   id_utilizador, id_encomenda, id_categoria
            FROM notificacao
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_notificacao(titulo, descricao, lida, id_utilizador,
                        id_encomenda, id_categoria):
    if len(titulo) > 150:
        raise ValueError("O título não pode ultrapassar 150 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO notificacao (
                titulo, descricao, lida, id_utilizador,
                id_encomenda, id_categoria
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [titulo, descricao, lida, id_utilizador,
              id_encomenda, id_categoria])


def atualizar_notificacao(id, titulo, descricao, lida, id_utilizador,
                          id_encomenda, id_categoria):
    if len(titulo) > 150:
        raise ValueError("O título não pode ultrapassar 150 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE notificacao
            SET titulo = %s,
                descricao = %s,
                lida = %s,
                id_utilizador = %s,
                id_encomenda = %s,
                id_categoria = %s
            WHERE id = %s
        """, [titulo, descricao, lida, id_utilizador,
              id_encomenda, id_categoria, id])


def eliminar_notificacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM notificacao
            WHERE id = %s
        """, [id])
