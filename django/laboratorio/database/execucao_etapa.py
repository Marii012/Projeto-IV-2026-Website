from django.db import connection


def listar_execucoes_etapa():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, data_inicio, data_fim,
                   id_pedido_trabalho, id_etapa, id_colaborador
            FROM execucao_etapa
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_execucao_etapa(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, data_inicio, data_fim,
                   id_pedido_trabalho, id_etapa, id_colaborador
            FROM execucao_etapa
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_execucao_etapa(
    data_inicio, data_fim, id_pedido_trabalho,
    id_etapa, id_colaborador
):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO execucao_etapa (
                data_inicio, data_fim, id_pedido_trabalho,
                id_etapa, id_colaborador
            )
            VALUES (%s, %s, %s, %s, %s)
        """, [
            data_inicio, data_fim, id_pedido_trabalho,
            id_etapa, id_colaborador
        ])


def atualizar_execucao_etapa(
    id, data_inicio, data_fim, id_pedido_trabalho,
    id_etapa, id_colaborador
):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE execucao_etapa
            SET data_inicio = %s,
                data_fim = %s,
                id_pedido_trabalho = %s,
                id_etapa = %s,
                id_colaborador = %s
            WHERE id = %s
        """, [
            data_inicio, data_fim, id_pedido_trabalho,
            id_etapa, id_colaborador, id
        ])


def eliminar_execucao_etapa(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM execucao_etapa
            WHERE id = %s
        """, [id])
