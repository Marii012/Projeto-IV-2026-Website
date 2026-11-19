import json
from functools import wraps

from django.contrib.auth.hashers import check_password
from django.core import signing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

# Funções que as colegas já escreveram (não alteramos nada nelas)
from laboratorio.database.cliente import listar_clientes
from laboratorio.database.encomenda import listar_encomendas
from laboratorio.database.estado import listar_estados
from laboratorio.database.pedido_trabalho import listar_pedidos_trabalho
from laboratorio.database.tipo_trabalho import listar_tipos_trabalho
from laboratorio.database.tipo_utilizador import obter_tipo_utilizador
from laboratorio.database.utilizador import obter_utilizador_por_email

SAL = 'app-movel'
TOKEN_MAX_IDADE = 60 * 60 * 24 * 7  # o token vale 7 dias


def json_pt(dados, status=200):
    """JsonResponse que mantém os acentos."""
    return JsonResponse(dados, safe=False, status=status,
                        json_dumps_params={'ensure_ascii': False})


def formatar_data(valor):
    """Aceita date, datetime ou texto 'AAAA-MM-DD...' e devolve 'DD/MM/AAAA'."""
    if not valor:
        return '—'
    ano, mes, dia = str(valor)[:10].split('-')
    return f'{dia}/{mes}/{ano}'


def perfil_do_tipo(id_tipo_utilizador):
    """Converte o tipo de utilizador da BD em 'administrador', 'cliente' ou 'colaborador'."""
    tipo = obter_tipo_utilizador(id_tipo_utilizador)  # (id, descricao)
    descricao = str(tipo[1]).lower() if tipo else ''
    if 'admin' in descricao:
        return 'administrador'
    if 'cliente' in descricao:
        return 'cliente'
    return 'colaborador'


def exige_token(view):
    """Só deixa passar pedidos com um token válido. Guarda o utilizador em request.utilizador."""
    @wraps(view)
    def envolvida(request, *args, **kwargs):
        cabecalho = request.headers.get('Authorization', '')
        if not cabecalho.startswith('Token '):
            return json_pt({'erro': 'Sem token'}, 401)
        try:
            request.utilizador = signing.loads(
                cabecalho[6:], salt=SAL, max_age=TOKEN_MAX_IDADE
            )
        except signing.BadSignature:  # também apanha o token expirado
            return json_pt({'erro': 'Token inválido'}, 401)
        return view(request, *args, **kwargs)
    return envolvida


@csrf_exempt
@require_POST
def login(request):
    try:
        dados = json.loads(request.body)
    except ValueError:
        return json_pt({'erro': 'JSON inválido'}, 400)

    email = str(dados.get('email', '')).strip()
    password = str(dados.get('password', ''))

    # (id, nome, email, password_hash, cargo, data_registo, id_tipo_utilizador, id_estado)
    utilizador = obter_utilizador_por_email(email)
    if utilizador is None or not check_password(password, utilizador[3]):
        return json_pt({'erro': 'Credenciais inválidas'}, 401)

    perfil = perfil_do_tipo(utilizador[6])
    token = signing.dumps({'id': utilizador[0], 'perfil': perfil}, salt=SAL)
    return json_pt({'token': token, 'nome': utilizador[1], 'perfil': perfil})


@require_GET
@exige_token
def encomendas_api(request):
    utilizador = request.utilizador  # {'id': ..., 'perfil': ...}

    clientes = listar_clientes()  # (id, nome, nif, telefone, data_aprovacao, id_utilizador)
    nome_cliente = {c[0]: c[1] for c in clientes}
    estados = {e[0]: e[1] for e in listar_estados()}
    tipos = {t[0]: t[1] for t in listar_tipos_trabalho()}

    # Trabalhos de cada encomenda: id_encomenda -> ['Prótese Fixa', ...]
    trabalhos = {}
    for p in listar_pedidos_trabalho():  # p[9] = id_encomenda, p[10] = id_tipo_trabalho
        trabalhos.setdefault(p[9], []).append(tipos.get(p[10], ''))

    encomendas = listar_encomendas()
    if utilizador['perfil'] == 'cliente':
        # O cliente só vê as encomendas dele (cliente.id_utilizador = o utilizador do token)
        ids_cliente = [c[0] for c in clientes if c[5] == utilizador['id']]
        encomendas = [e for e in encomendas if e[12] in ids_cliente]  # e[12] = id_cliente

    dados = []
    for e in encomendas:
        # e[0] = id, e[1] = cliente_nome_avulso, e[10] = data_limite,
        # e[12] = id_cliente, e[16] = id_estado
        dados.append({
            'codigo': f'ENC-{e[0]:03d}',
            'clinica': nome_cliente.get(e[12]) or e[1] or '',
            'estado': estados.get(e[16], ''),
            'trabalho': ', '.join(t for t in trabalhos.get(e[0], []) if t),
            'prazo': formatar_data(e[10]),
        })
    return json_pt(dados)