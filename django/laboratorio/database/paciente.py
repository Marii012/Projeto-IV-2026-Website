from django.db import connection


def listar_pacientes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, identificador, sexo
            FROM paciente
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_paciente(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, identificador, sexo
            FROM paciente
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_paciente(identificador, sexo):
    if len(identificador) > 60:
        raise ValueError("O identificador não pode ultrapassar 60 caracteres.")

    if len(sexo) > 1:
        raise ValueError("O sexo só pode ter 1 carácter.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO paciente (identificador, sexo)
            VALUES (%s, %s)
        """, [identificador, sexo])


def atualizar_paciente(id, identificador, sexo):
    if len(identificador) > 60:
        raise ValueError("O identificador não pode ultrapassar 60 caracteres.")

    if len(sexo) > 1:
        raise ValueError("O sexo só pode ter 1 carácter.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE paciente
            SET identificador = %s,
                sexo = %s
            WHERE id = %s
        """, [identificador, sexo, id])


def eliminar_paciente(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM paciente
            WHERE id = %s
        """, [id])
