from django.db import connection


def listar_ficheiros():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, caminho, versao, visivel_cliente, data,
                   id_encomenda, id_nota, id_enviado_por,
                   id_tipo_ficheiro, id_estado
            FROM ficheiro
            ORDER BY data DESC
        """)
        return cursor.fetchall()


def obter_ficheiro(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, caminho, versao, visivel_cliente, data,
                   id_encomenda, id_nota, id_enviado_por,
                   id_tipo_ficheiro, id_estado
            FROM ficheiro
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_ficheiro(
    caminho, versao, visivel_cliente, id_encomenda,
    id_nota, id_enviado_por, id_tipo_ficheiro, id_estado
):
    if len(caminho) > 500:
        raise ValueError("O caminho não pode ultrapassar 500 caracteres.")

    if not 0 <= versao <= 32767:
        raise ValueError("Versão inválida.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ficheiro (
                caminho, versao, visivel_cliente,
                id_encomenda, id_nota, id_enviado_por,
                id_tipo_ficheiro, id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [
            caminho, versao, visivel_cliente,
            id_encomenda, id_nota, id_enviado_por,
            id_tipo_ficheiro, id_estado
        ])


def atualizar_ficheiro(
    id, caminho, versao, visivel_cliente, id_encomenda,
    id_nota, id_enviado_por, id_tipo_ficheiro, id_estado
):
    if len(caminho) > 500:
        raise ValueError("O caminho não pode ultrapassar 500 caracteres.")

    if not 0 <= versao <= 32767:
        raise ValueError("Versão inválida.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE ficheiro
            SET caminho = %s,
                versao = %s,
                visivel_cliente = %s,
                id_encomenda = %s,
                id_nota = %s,
                id_enviado_por = %s,
                id_tipo_ficheiro = %s,
                id_estado = %s
            WHERE id = %s
        """, [
            caminho, versao, visivel_cliente,
            id_encomenda, id_nota, id_enviado_por,
            id_tipo_ficheiro, id_estado, id
        ])


def eliminar_ficheiro(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM ficheiro
            WHERE id = %s
        """, [id])
