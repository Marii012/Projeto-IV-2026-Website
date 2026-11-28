from django.db import connection


def listar_solicitacoes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, data_pedido, data_decisao,
                   id_encomenda, id_solicitante, id_decisor,
                   id_tipo_solicitacao, id_motivo, id_estado
            FROM solicitacao
            ORDER BY data_pedido DESC
        """)
        return cursor.fetchall()


def obter_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, data_pedido, data_decisao,
                   id_encomenda, id_solicitante, id_decisor,
                   id_tipo_solicitacao, id_motivo, id_estado
            FROM solicitacao
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_solicitacao(descricao, data_decisao, id_encomenda,
                        id_solicitante, id_decisor, id_tipo_solicitacao,
                        id_motivo, id_estado):

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO solicitacao (
                descricao, data_decisao, id_encomenda,
                id_solicitante, id_decisor, id_tipo_solicitacao,
                id_motivo, id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [descricao, data_decisao, id_encomenda,
              id_solicitante, id_decisor, id_tipo_solicitacao,
              id_motivo, id_estado])


def atualizar_solicitacao(id, descricao, data_decisao, id_encomenda,
                          id_solicitante, id_decisor, id_tipo_solicitacao,
                          id_motivo, id_estado):

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE solicitacao
            SET descricao = %s,
                data_decisao = %s,
                id_encomenda = %s,
                id_solicitante = %s,
                id_decisor = %s,
                id_tipo_solicitacao = %s,
                id_motivo = %s,
                id_estado = %s
            WHERE id = %s
        """, [descricao, data_decisao, id_encomenda,
              id_solicitante, id_decisor, id_tipo_solicitacao,
              id_motivo, id_estado, id])


def eliminar_solicitacao(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM solicitacao
            WHERE id = %s
        """, [id])

def criar_solicitacao(id_encomenda, id_solicitante,
                      id_tipo_solicitacao, id_motivo,
                      descricao, trabalhos):

    with connection.cursor() as cursor:
        cursor.execute("""
            CALL sp_criar_solicitacao(%s, %s, %s, %s, %s, %s, %s)
        """, [
            id_encomenda,
            id_solicitante,
            id_tipo_solicitacao,
            id_motivo,
            descricao,
            trabalhos,
            None
        ])

        resultado = cursor.fetchone()
        return resultado[0]


def decidir_solicitacao(id_solicitacao, id_decisor, aprovar):

    with connection.cursor() as cursor:
        cursor.execute("""
            CALL sp_decidir_solicitacao(%s, %s, %s, %s)
        """, [
            id_solicitacao,
            id_decisor,
            aprovar,
            None
        ])

        resultado = cursor.fetchone()
        return resultado[0]

def listar_solicitacoes_cliente(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, data_pedido, data_decisao,
                   id_encomenda, id_solicitante, id_decisor,
                   id_tipo_solicitacao, id_motivo, id_estado
            FROM solicitacao
            WHERE id_solicitante = %s
            ORDER BY data_pedido DESC
        """, [id_utilizador])

        return cursor.fetchall()


def obter_solicitacao_cliente(id, id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, data_pedido, data_decisao,
                   id_encomenda, id_solicitante, id_decisor,
                   id_tipo_solicitacao, id_motivo, id_estado
            FROM solicitacao
            WHERE id = %s AND id_solicitante = %s
        """, [id, id_utilizador])

        return cursor.fetchone()