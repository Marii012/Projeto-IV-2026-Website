from django.db import connection, transaction
from django.contrib.auth.hashers import make_password


def listar_utilizadores():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, password_hash, cargo,
                   data_registo, id_tipo_utilizador, id_estado
            FROM utilizador
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_utilizador(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, password_hash, cargo,
                   data_registo, id_tipo_utilizador, id_estado
            FROM utilizador
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def obter_utilizador_por_email(email):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, email, password_hash, cargo,
                   data_registo, id_tipo_utilizador, id_estado
            FROM utilizador
            WHERE LOWER(email) = LOWER(%s)
        """, [email])

        return cursor.fetchone()


def inserir_utilizador(nome, email, password, cargo,
                       id_tipo_utilizador, id_estado):

    if len(nome) > 100:
        raise ValueError("O nome não pode ultrapassar 100 caracteres.")

    if len(email) > 150:
        raise ValueError("O email não pode ultrapassar 150 caracteres.")

    if cargo is not None and len(cargo) > 60:
        raise ValueError("O cargo não pode ultrapassar 60 caracteres.")

    # Se não existir palavra-passe, criar uma conta sem password utilizável.
    password_hash = make_password(password)

    if len(password_hash) > 255:
        raise ValueError("A password hash não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO utilizador (
                nome, email, password_hash, cargo,
                id_tipo_utilizador, id_estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, [
            nome, email, password_hash, cargo,
            id_tipo_utilizador, id_estado
        ])

        resultado = cursor.fetchone()
        return resultado[0]


def inserir_cliente(id_utilizador, nome, nif, telefone):

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO cliente (
                id_utilizador, nome, nif, telefone
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, [id_utilizador, nome, nif, telefone])

        resultado = cursor.fetchone()
        return resultado[0]


def inserir_morada(id_cliente, nome_clinica, morada):

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO morada (
                id_cliente, nome_clinica, morada
            )
            VALUES (%s, %s, %s)
        """, [id_cliente, nome_clinica, morada])


def atualizar_utilizador(id, nome, email, password, cargo,
                         id_tipo_utilizador, id_estado):

    if len(nome) > 100:
        raise ValueError("O nome não pode ultrapassar 100 caracteres.")

    if len(email) > 150:
        raise ValueError("O email não pode ultrapassar 150 caracteres.")

    if cargo is not None and len(cargo) > 60:
        raise ValueError("O cargo não pode ultrapassar 60 caracteres.")

    with connection.cursor() as cursor:

        if password:
            password_hash = make_password(password)

            if len(password_hash) > 255:
                raise ValueError("A password hash não pode ultrapassar 255 caracteres.")

            cursor.execute("""
                UPDATE utilizador
                SET nome = %s,
                    email = %s,
                    password_hash = %s,
                    cargo = %s,
                    id_tipo_utilizador = %s,
                    id_estado = %s
                WHERE id = %s
            """, [
                nome, email, password_hash, cargo,
                id_tipo_utilizador, id_estado, id
            ])

        else:
            cursor.execute("""
                UPDATE utilizador
                SET nome = %s,
                    email = %s,
                    cargo = %s,
                    id_tipo_utilizador = %s,
                    id_estado = %s
                WHERE id = %s
            """, [
                nome, email, cargo,
                id_tipo_utilizador, id_estado, id
            ])

        return cursor.rowcount


def eliminar_utilizador(id):

    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM utilizador
            WHERE id = %s
        """, [id])

        return cursor.rowcount
