from django.db import connection


def listar_pedidos_trabalho():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, e_digital, material_da_clinica, material_desc,
                   material_qtd, material_obs, cor, dentes,
                   data_proxima_consulta, id_encomenda,
                   id_tipo_trabalho, id_estado, id_material
            FROM pedido_trabalho
            ORDER BY id
        """)
        return cursor.fetchall()


def obter_pedido_trabalho(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, e_digital, material_da_clinica, material_desc,
                   material_qtd, material_obs, cor, dentes,
                   data_proxima_consulta, id_encomenda,
                   id_tipo_trabalho, id_estado, id_material
            FROM pedido_trabalho
            WHERE id = %s
        """, [id])
        return cursor.fetchone()


def inserir_pedido_trabalho(e_digital, material_da_clinica, material_desc,
                            material_qtd, material_obs, cor, dentes,
                            data_proxima_consulta, id_encomenda,
                            id_tipo_trabalho, id_estado, id_material):

    if material_desc is not None and len(material_desc) > 255:
        raise ValueError("A descrição do material não pode ultrapassar 255 caracteres.")

    if material_qtd is not None and len(material_qtd) > 50:
        raise ValueError("A quantidade de material não pode ultrapassar 50 caracteres.")

    if cor is not None and len(cor) > 50:
        raise ValueError("A cor não pode ultrapassar 50 caracteres.")

    if dentes is not None and len(dentes) > 100:
        raise ValueError("A informação dos dentes não pode ultrapassar 100 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO pedido_trabalho (
                e_digital, material_da_clinica, material_desc,
                material_qtd, material_obs, cor, dentes,
                data_proxima_consulta, id_encomenda,
                id_tipo_trabalho, id_estado, id_material
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, [e_digital, material_da_clinica, material_desc,
              material_qtd, material_obs, cor, dentes,
              data_proxima_consulta, id_encomenda,
              id_tipo_trabalho, id_estado, id_material])


def atualizar_pedido_trabalho(id, e_digital, material_da_clinica,
                              material_desc, material_qtd, material_obs,
                              cor, dentes, data_proxima_consulta,
                              id_encomenda, id_tipo_trabalho,
                              id_estado, id_material):

    if material_desc is not None and len(material_desc) > 255:
        raise ValueError("A descrição do material não pode ultrapassar 255 caracteres.")

    if material_qtd is not None and len(material_qtd) > 50:
        raise ValueError("A quantidade de material não pode ultrapassar 50 caracteres.")

    if cor is not None and len(cor) > 50:
        raise ValueError("A cor não pode ultrapassar 50 caracteres.")

    if dentes is not None and len(dentes) > 100:
        raise ValueError("A informação dos dentes não pode ultrapassar 100 caracteres.")

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE pedido_trabalho
            SET e_digital = %s,
                material_da_clinica = %s,
                material_desc = %s,
                material_qtd = %s,
                material_obs = %s,
                cor = %s,
                dentes = %s,
                data_proxima_consulta = %s,
                id_encomenda = %s,
                id_tipo_trabalho = %s,
                id_estado = %s,
                id_material = %s
            WHERE id = %s
        """, [e_digital, material_da_clinica, material_desc,
              material_qtd, material_obs, cor, dentes,
              data_proxima_consulta, id_encomenda,
              id_tipo_trabalho, id_estado, id_material, id])


def eliminar_pedido_trabalho(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM pedido_trabalho
            WHERE id = %s
        """, [id])

def listar_pedidos_trabalho_cliente(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pt.id, pt.e_digital, pt.material_da_clinica,
                   pt.material_desc, pt.material_qtd, pt.material_obs,
                   pt.cor, pt.dentes, pt.data_proxima_consulta,
                   pt.id_encomenda, pt.id_tipo_trabalho,
                   pt.id_estado, pt.id_material
            FROM pedido_trabalho pt
            INNER JOIN encomenda e ON e.id = pt.id_encomenda
            INNER JOIN cliente c ON c.id = e.id_cliente
            WHERE c.id_utilizador = %s
            ORDER BY pt.id
        """, [id_utilizador])

        return cursor.fetchall()


def obter_pedido_trabalho_cliente(id, id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pt.id, pt.e_digital, pt.material_da_clinica,
                   pt.material_desc, pt.material_qtd, pt.material_obs,
                   pt.cor, pt.dentes, pt.data_proxima_consulta,
                   pt.id_encomenda, pt.id_tipo_trabalho,
                   pt.id_estado, pt.id_material
            FROM pedido_trabalho pt
            INNER JOIN encomenda e ON e.id = pt.id_encomenda
            INNER JOIN cliente c ON c.id = e.id_cliente
            WHERE pt.id = %s AND c.id_utilizador = %s
        """, [id, id_utilizador])

        return cursor.fetchone()
