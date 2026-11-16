from django.db import connection


def listar_tipos_trabalho():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, detalhe, ativo
            FROM tipo_trabalho
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_tipo_trabalho(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, descricao, detalhe, ativo
            FROM tipo_trabalho
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_tipo_trabalho(descricao, detalhe, ativo):
    if len(descricao) > 80:
        raise ValueError("A descrição não pode ultrapassar 80 caracteres.")

    if detalhe is not None and len(detalhe) > 255:
        raise ValueError("O detalhe não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO tipo_trabalho (descricao, detalhe, ativo)
            VALUES (%s, %s, %s)
        """, [descricao, detalhe, ativo])


def atualizar_tipo_trabalho(id, descricao, detalhe, ativo):
    if len(descricao) > 80:
        raise ValueError("A descrição não pode ultrapassar 80 caracteres.")

    if detalhe is not None and len(detalhe) > 255:
        raise ValueError("O detalhe não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE tipo_trabalho
            SET descricao = %s,
                detalhe = %s,
                ativo = %s
            WHERE id = %s
        """, [descricao, detalhe, ativo, id])


def eliminar_tipo_trabalho(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM tipo_trabalho
            WHERE id = %s
        """, [id])
