"""Utilizadores. O password_hash nunca sai deste módulo para a API pública."""
from app.repositories.base import ErroValidacao
from app.seguranca import gerar_hash

# Colunas que podem ser devolvidas ao exterior (sem password_hash).
PUBLICAS = "id, nome, email, cargo, data_registo, id_tipo_utilizador, id_estado"


def _validar(nome, email, cargo):
    if nome is None or len(nome) > 100:
        raise ErroValidacao("O nome não pode ultrapassar 100 caracteres.")
    if email is None or len(email) > 150:
        raise ErroValidacao("O email não pode ultrapassar 150 caracteres.")
    if cargo is not None and len(cargo) > 60:
        raise ErroValidacao("O cargo não pode ultrapassar 60 caracteres.")


def listar(cur):
    cur.execute(f"SELECT {PUBLICAS} FROM utilizador ORDER BY id")
    return cur.fetchall()


def obter(cur, id):
    cur.execute(f"SELECT {PUBLICAS} FROM utilizador WHERE id = %s", [id])
    return cur.fetchone()


def obter_por_email_com_hash(cur, email):
    """Só para o login: inclui o password_hash."""
    cur.execute(
        f"SELECT {PUBLICAS}, password_hash FROM utilizador WHERE LOWER(email) = LOWER(%s)",
        [email])
    return cur.fetchone()


def inserir(cur, nome, email, password, cargo, id_tipo_utilizador, id_estado):
    _validar(nome, email, cargo)
    cur.execute(
        """
        INSERT INTO utilizador (nome, email, password_hash, cargo,
                                id_tipo_utilizador, id_estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        [nome, email, gerar_hash(password), cargo, id_tipo_utilizador, id_estado])
    return cur.fetchone()["id"]


def atualizar(cur, id, nome, email, password, cargo, id_tipo_utilizador, id_estado):
    """A password só é alterada se for enviada (None mantém a atual)."""
    _validar(nome, email, cargo)
    cur.execute(
        """
        UPDATE utilizador
        SET nome = %s, email = %s, cargo = %s,
            id_tipo_utilizador = %s, id_estado = %s,
            password_hash = COALESCE(%s, password_hash)
        WHERE id = %s
        RETURNING id
        """,
        [nome, email, cargo, id_tipo_utilizador, id_estado,
         gerar_hash(password) if password else None, id])
    return cur.fetchone() is not None


def eliminar(cur, id):
    cur.execute("DELETE FROM utilizador WHERE id = %s RETURNING 1", [id])
    return cur.fetchone() is not None


def obter_id_cliente(cur, id_utilizador):
    cur.execute("SELECT id FROM cliente WHERE id_utilizador = %s", [id_utilizador])
    linha = cur.fetchone()
    return linha["id"] if linha else None


def contar_por_tipo(cur, id_tipo):
    cur.execute(
        "SELECT COUNT(*) AS total FROM utilizador WHERE id_tipo_utilizador = %s",
        [id_tipo])
    return cur.fetchone()["total"]


def listar_por_tipo(cur, id_tipo, pesquisa=""):
    """Listagem do painel de administração (com estado, NIF e pesquisa)."""
    q = """
        SELECT u.id, u.nome, u.email, e.descricao AS estado,
               c.nif, 0 AS total_trabalhos
        FROM utilizador u
        LEFT JOIN cliente c ON c.id_utilizador = u.id
        LEFT JOIN estado e ON e.id = u.id_estado
        WHERE u.id_tipo_utilizador = %s
    """
    params = [id_tipo]
    if pesquisa:
        q += """
            AND (u.nome ILIKE %s OR u.email ILIKE %s
                 OR CAST(c.nif AS TEXT) ILIKE %s)
        """
        params += [f"%{pesquisa}%"] * 3
    q += " ORDER BY u.nome ASC"
    cur.execute(q, params)
    return cur.fetchall()
