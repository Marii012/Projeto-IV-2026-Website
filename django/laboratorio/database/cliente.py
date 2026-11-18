from django.db import connection


def listar_clientes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, nif, telefone, data_aprovacao, id_utilizador
            FROM cliente
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_cliente(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, nif, telefone, data_aprovacao, id_utilizador
            FROM cliente
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_cliente(nome, nif, telefone, data_aprovacao, id_utilizador):
    if len(nome) > 120:
        raise ValueError("O nome não pode ultrapassar 120 caracteres.")

    if len(nif) != 9:
        raise ValueError("O NIF deve ter exatamente 9 caracteres.")

    if telefone and len(telefone) > 20:
        raise ValueError("O telefone não pode ultrapassar 20 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO cliente
                (nome, nif, telefone, data_aprovacao, id_utilizador)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, [nome, nif, telefone, data_aprovacao, id_utilizador])

        resultado = cursor.fetchone()

        return resultado[0]


def atualizar_cliente(id, nome, nif, telefone, data_aprovacao, id_utilizador):
    if len(nome) > 120:
        raise ValueError("O nome não pode ultrapassar 120 caracteres.")

    if len(nif) != 9:
        raise ValueError("O NIF deve ter exatamente 9 caracteres.")

    if telefone and len(telefone) > 20:
        raise ValueError("O telefone não pode ultrapassar 20 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE cliente
            SET nome = %s,
                nif = %s,
                telefone = %s,
                data_aprovacao = %s,
                id_utilizador = %s
            WHERE id = %s
        """, [nome, nif, telefone, data_aprovacao, id_utilizador, id])


def eliminar_cliente(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM cliente
            WHERE id = %s
        """, [id])
