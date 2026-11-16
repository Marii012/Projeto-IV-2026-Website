from django.db import connection


def listar_etapas():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, designacao, ordem, e_administrativa,
                   limite_cancelamento, id_tipo_trabalho
            FROM etapa
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_etapa(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, designacao, ordem, e_administrativa,
                   limite_cancelamento, id_tipo_trabalho
            FROM etapa
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_etapa(
    designacao, ordem, e_administrativa,
    limite_cancelamento, id_tipo_trabalho
):
    if len(designacao) > 100:
        raise ValueError("A designação não pode ultrapassar 100 caracteres.")

    if ordem is not None and not -32768 <= ordem <= 32767:
        raise ValueError("A ordem está fora dos limites permitidos.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO etapa (
                designacao, ordem, e_administrativa,
                limite_cancelamento, id_tipo_trabalho
            )
            VALUES (%s, %s, %s, %s, %s)
        """, [
            designacao, ordem, e_administrativa,
            limite_cancelamento, id_tipo_trabalho
        ])


def atualizar_etapa(
    id, designacao, ordem, e_administrativa,
    limite_cancelamento, id_tipo_trabalho
):
    if len(designacao) > 100:
        raise ValueError("A designação não pode ultrapassar 100 caracteres.")

    if ordem is not None and not -32768 <= ordem <= 32767:
        raise ValueError("A ordem está fora dos limites permitidos.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE etapa
            SET designacao = %s,
                ordem = %s,
                e_administrativa = %s,
                limite_cancelamento = %s,
                id_tipo_trabalho = %s
            WHERE id = %s
        """, [
            designacao, ordem, e_administrativa,
            limite_cancelamento, id_tipo_trabalho, id
        ])


def eliminar_etapa(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM etapa
            WHERE id = %s
        """, [id])
