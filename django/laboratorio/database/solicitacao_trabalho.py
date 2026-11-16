from django.db import connection


def listar_solicitacoes_trabalho():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_solicitacao, id_pedido_trabalho
            FROM solicitacao_trabalho
            ORDER BY id_solicitacao
        """)
        return cursor.fetchall()


def obter_solicitacao_trabalho(id_solicitacao, id_pedido_trabalho):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_solicitacao, id_pedido_trabalho
            FROM solicitacao_trabalho
            WHERE id_solicitacao = %s
              AND id_pedido_trabalho = %s
        """, [id_solicitacao, id_pedido_trabalho])
        return cursor.fetchone()


def inserir_solicitacao_trabalho(id_solicitacao, id_pedido_trabalho):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO solicitacao_trabalho (
                id_solicitacao, id_pedido_trabalho
            )
            VALUES (%s, %s)
        """, [id_solicitacao, id_pedido_trabalho])


def atualizar_solicitacao_trabalho(id_solicitacao, id_pedido_trabalho,
                                   novo_id_solicitacao, novo_id_pedido_trabalho):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE solicitacao_trabalho
            SET id_solicitacao = %s,
                id_pedido_trabalho = %s
            WHERE id_solicitacao = %s
              AND id_pedido_trabalho = %s
        """, [novo_id_solicitacao, novo_id_pedido_trabalho,
              id_solicitacao, id_pedido_trabalho])


def eliminar_solicitacao_trabalho(id_solicitacao, id_pedido_trabalho):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM solicitacao_trabalho
            WHERE id_solicitacao = %s
              AND id_pedido_trabalho = %s
        """, [id_solicitacao, id_pedido_trabalho])
