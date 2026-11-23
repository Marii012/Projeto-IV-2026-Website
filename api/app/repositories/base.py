"""Base comum dos repositórios: SQL parametrizado + validações por coluna.

Cada tabela declara as suas colunas (com limites) e herda listar / obter /
inserir / atualizar / eliminar. É o equivalente aos antigos ficheiros
django/laboratorio/database/*.py.
"""
from dataclasses import dataclass
from typing import Any, Optional

from psycopg2 import sql
from pydantic import create_model


class ErroValidacao(ValueError):
    """Dados inválidos (a API devolve 400 com a mensagem)."""


@dataclass(frozen=True)
class Coluna:
    nome: str
    tipo: Any = Any
    rotulo: str = ""            # ex.: "O nome" (usado nas mensagens de erro)
    max_len: Optional[int] = None
    tam_exato: Optional[int] = None
    minimo: Optional[int] = None
    maximo: Optional[int] = None
    obrigatoria: bool = False
    msg: Optional[str] = None   # mensagem personalizada para violações de limite


def texto(nome, rotulo, max_len=None, obrigatoria=False, tam_exato=None, msg=None):
    return Coluna(nome, str, rotulo, max_len=max_len, tam_exato=tam_exato,
                  obrigatoria=obrigatoria, msg=msg)


def inteiro(nome, rotulo="", minimo=None, maximo=None, obrigatoria=False, msg=None):
    return Coluna(nome, int, rotulo, minimo=minimo, maximo=maximo,
                  obrigatoria=obrigatoria, msg=msg)


def ref(nome, obrigatoria=False):
    """Chave estrangeira (id inteiro)."""
    return Coluna(nome, int, obrigatoria=obrigatoria)


def livre(nome, obrigatoria=False):
    """Coluna sem limites conhecidos (datas, booleanos, texto longo...)."""
    return Coluna(nome, Any, obrigatoria=obrigatoria)


class Tabela:
    def __init__(self, nome, colunas, pk=("id",), so_leitura=(), ordem="id",
                 restricao=None):
        self.nome = nome
        self.colunas = list(colunas)
        self.pk = tuple(pk)
        self.so_leitura = tuple(so_leitura)
        self.ordem = ordem
        # {tipo_utilizador: (coluna, "chave do token")} -> filtra linhas por dono
        self.restricao = restricao or {}

    # ------------------------------------------------------------------ SQL
    @property
    def _select(self):
        nomes = list(self.pk) + [c.nome for c in self.colunas] + list(self.so_leitura)
        return sql.SQL(", ").join(sql.Identifier(n) for n in nomes)

    def _where(self, pk_valores, filtro):
        partes = [sql.SQL("{} = %s").format(sql.Identifier(c)) for c in self.pk]
        valores = list(pk_valores)
        if filtro:
            partes.append(sql.SQL("{} = %s").format(sql.Identifier(filtro[0])))
            valores.append(filtro[1])
        return sql.SQL(" AND ").join(partes), valores

    def listar(self, cur, filtro=None):
        q = sql.SQL("SELECT {} FROM {}").format(self._select, sql.Identifier(self.nome))
        valores = []
        if filtro:
            q += sql.SQL(" WHERE {} = %s").format(sql.Identifier(filtro[0]))
            valores.append(filtro[1])
        q += sql.SQL(" ORDER BY ") + sql.SQL(self.ordem)  # `ordem` é constante do código
        cur.execute(q, valores)
        return cur.fetchall()

    def obter(self, cur, pk_valores, filtro=None):
        where, valores = self._where(pk_valores, filtro)
        cur.execute(
            sql.SQL("SELECT {} FROM {} WHERE {}").format(
                self._select, sql.Identifier(self.nome), where),
            valores)
        return cur.fetchone()

    def inserir(self, cur, dados):
        """Insere só os campos fornecidos (os restantes usam o DEFAULT da BD)."""
        dados = self.validar(dados)
        nomes = [p for p in self.pk if p in dados]
        nomes += [c.nome for c in self.colunas if c.nome in dados]
        if nomes:
            q = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING {}").format(
                sql.Identifier(self.nome),
                sql.SQL(", ").join(sql.Identifier(n) for n in nomes),
                sql.SQL(", ").join(sql.Placeholder() for _ in nomes),
                self._select)
        else:
            q = sql.SQL("INSERT INTO {} DEFAULT VALUES RETURNING {}").format(
                sql.Identifier(self.nome), self._select)
        cur.execute(q, [dados[n] for n in nomes])
        return cur.fetchone()

    def atualizar(self, cur, pk_valores, dados, filtro=None):
        """Atualização parcial: só altera os campos enviados."""
        dados = self.validar(dados, parcial=True)
        colunas = [c.nome for c in self.colunas if c.nome in dados]
        if not colunas:
            raise ErroValidacao("Indica pelo menos um campo para atualizar.")
        where, valores_where = self._where(pk_valores, filtro)
        sets = sql.SQL(", ").join(
            sql.SQL("{} = %s").format(sql.Identifier(n)) for n in colunas)
        cur.execute(
            sql.SQL("UPDATE {} SET {} WHERE {} RETURNING {}").format(
                sql.Identifier(self.nome), sets, where, self._select),
            [dados[n] for n in colunas] + valores_where)
        return cur.fetchone()

    def eliminar(self, cur, pk_valores, filtro=None):
        where, valores = self._where(pk_valores, filtro)
        cur.execute(
            sql.SQL("DELETE FROM {} WHERE {} RETURNING 1").format(
                sql.Identifier(self.nome), where),
            valores)
        return cur.fetchone() is not None

    # ----------------------------------------------------------- validação
    def validar(self, dados, parcial=False):
        for c in self.colunas:
            if parcial and c.nome not in dados:
                continue
            v = dados.get(c.nome)
            if v is None:
                if c.obrigatoria:
                    raise ErroValidacao(f"O campo '{c.nome}' é obrigatório.")
                continue
            if c.tipo is str:
                if c.tam_exato is not None and len(v) != c.tam_exato:
                    raise ErroValidacao(
                        c.msg or f"{c.rotulo} deve ter exatamente {c.tam_exato} caracteres.")
                if c.max_len is not None and len(v) > c.max_len:
                    raise ErroValidacao(
                        c.msg or f"{c.rotulo} não pode ultrapassar {c.max_len} caracteres.")
            elif c.tipo is int:
                if (c.minimo is not None and v < c.minimo) or (
                        c.maximo is not None and v > c.maximo):
                    raise ErroValidacao(
                        c.msg or f"{c.rotulo} está fora dos limites permitidos.")
        return dados

    # ------------------------------------------------- modelo (documentação)
    def modelo(self, parcial=False):
        """Modelo pydantic do corpo do pedido (também alimenta o /docs)."""
        campos = {}
        for c in self.colunas:
            if c.obrigatoria and not parcial:
                campos[c.nome] = (c.tipo, ...)
            else:
                campos[c.nome] = (Optional[c.tipo], None)
        sufixo = "Update" if parcial else "In"
        return create_model(f"{self.nome.title().replace('_', '')}{sufixo}", **campos)
