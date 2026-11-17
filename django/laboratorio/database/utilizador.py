from django.db import connection
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

    # Transformar a palavra-passe num hash seguro
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
        """, [
            nome, email, password_hash, cargo,
            id_tipo_utilizador, id_estado
        ])


def atualizar_utilizador(id, nome, email, password, cargo,
                         id_tipo_utilizador, id_estado):

    if len(nome) > 100:
        raise ValueError("O nome não pode ultrapassar 100 caracteres.")

    if len(email) > 150:
        raise ValueError("O email não pode ultrapassar 150 caracteres.")

    if cargo is not None and len(cargo) > 60:
        raise ValueError("O cargo não pode ultrapassar 60 caracteres.")

    password_hash = make_password(password)

    if len(password_hash) > 255:
        raise ValueError("A password hash não pode ultrapassar 255 caracteres.")

    with connection.cursor() as cursor:
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


def eliminar_utilizador(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM utilizador
            WHERE id = %s
        """, [id])
