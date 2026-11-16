from django.db import connection


def listar_notas():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, texto, visivel_cliente, data,
                   id_encomenda, id_execucao_etapa, id_autor
            FROM nota
            ORDER BY data DESC
        """)
        return cursor.fetchall()


def obter_nota(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, texto, visivel_cliente, data,
                   id_encomenda, id_execucao_etapa, id_autor
            FROM nota
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_nota(texto, visivel_cliente, id_encomenda,
                 id_execucao_etapa, id_autor):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO nota (
                texto, visivel_cliente, id_encomenda,
                id_execucao_etapa, id_autor
            )
            VALUES (%s, %s, %s, %s, %s)
        """, [texto, visivel_cliente, id_encomenda,
              id_execucao_etapa, id_autor])


def atualizar_nota(id, texto, visivel_cliente, id_encomenda,
                   id_execucao_etapa, id_autor):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE nota
            SET texto = %s,
                visivel_cliente = %s,
                id_encomenda = %s,
                id_execucao_etapa = %s,
                id_autor = %s
            WHERE id = %s
        """, [texto, visivel_cliente, id_encomenda,
              id_execucao_etapa, id_autor, id])


def eliminar_nota(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM nota
            WHERE id = %s
        """, [id])
