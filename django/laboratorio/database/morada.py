from django.db import connection


def listar_moradas():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome_clinica, morada, id_cliente
            FROM morada
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_morada(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome_clinica, morada, id_cliente
            FROM morada
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_morada(nome_clinica, morada, id_cliente):
    if len(nome_clinica) > 120:
        raise ValueError("O nome da clínica não pode ultrapassar 120 caracteres.")

    if len(morada) > 255:
        raise ValueError("A morada não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO morada (nome_clinica, morada, id_cliente)
            VALUES (%s, %s, %s)
        """, [nome_clinica, morada, id_cliente])


def atualizar_morada(id, nome_clinica, morada, id_cliente):
    if len(nome_clinica) > 120:
        raise ValueError("O nome da clínica não pode ultrapassar 120 caracteres.")

    if len(morada) > 255:
        raise ValueError("A morada não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE morada
            SET nome_clinica = %s,
                morada = %s,
                id_cliente = %s
            WHERE id = %s
        """, [nome_clinica, morada, id_cliente, id])


def eliminar_morada(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM morada
            WHERE id = %s
        """, [id])
