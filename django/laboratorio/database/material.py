from django.db import connection


def listar_materiais():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, ativo
            FROM material
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_material(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nome, ativo
            FROM material
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_material(nome, ativo):
    if len(nome) > 80:
        raise ValueError("O nome não pode ultrapassar 80 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO material (nome, ativo)
            VALUES (%s, %s)
        """, [nome, ativo])


def atualizar_material(id, nome, ativo):
    if len(nome) > 80:
        raise ValueError("O nome não pode ultrapassar 80 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE material
            SET nome = %s,
                ativo = %s
            WHERE id = %s
        """, [nome, ativo, id])


def eliminar_material(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM material
            WHERE id = %s
        """, [id])
