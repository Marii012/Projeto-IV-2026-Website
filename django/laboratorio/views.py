from django.contrib import messages
from django.shortcuts import render, redirect

from laboratorio.permissoes import (
    DASHBOARD_POR_TIPO, requer_tipo, sessao_expirada
)
from laboratorio.services.api_client import ApiError, api


def home(request):
    return render(request, 'laboratorio/public/home.html')


def contacto(request):
    return redirect('/#contactos')


def entrar(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            resposta = api(
                'POST', '/auth/login',
                json={'email': email, 'password': password}
            )
        except ApiError as erro:
            messages.error(request, erro.detalhe)
            return render(request, 'laboratorio/auth/login.html')

        utilizador = resposta['utilizador']

        # Guardar na sessão o token da API e os dados do utilizador
        request.session['token'] = resposta['access_token']
        request.session['utilizador_id'] = utilizador['id']
        request.session['utilizador_nome'] = utilizador['nome']
        request.session['utilizador_email'] = utilizador['email']
        request.session['tipo_utilizador_id'] = utilizador['id_tipo_utilizador']

        # Encaminhar conforme o tipo de utilizador
        destino = DASHBOARD_POR_TIPO.get(utilizador['id_tipo_utilizador'])

        if destino:
            return redirect(destino)

        request.session.flush()
        messages.error(request, 'Tipo de utilizador não reconhecido.')
        return render(request, 'laboratorio/auth/login.html')

    return render(request, 'laboratorio/auth/login.html')


def registo(request):

    erro_registo = None

    if request.method == 'POST':

        moradas = [
            morada.strip()
            for morada in request.POST.getlist('morada[]')
            if morada.strip()
        ]

        # As validações e a gravação (utilizador + cliente + moradas,
        # numa só transação) são feitas pela API.
        dados = {
            'nome': request.POST.get('nome', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'telefone': request.POST.get('telefone', '').strip(),
            'nif': request.POST.get('nif', '').strip(),
            'password': request.POST.get('password', ''),
            'confirmar_password': request.POST.get('confirmar_password', ''),
            'moradas': moradas,
        }

        try:
            api('POST', '/auth/registo', json=dados)

            messages.success(
                request,
                'Pedido de registo enviado com sucesso! Aguarda a aprovação do administrador.'
            )

            return redirect('entrar')

        except ApiError as erro:
            erro_registo = erro.detalhe

    return render(
        request,
        'laboratorio/auth/registo.html',
        {
            'erro_registo': erro_registo,
            'dados_registo': request.POST,
            'moradas_registo': request.POST.getlist('morada[]') or ['']
        }
    )


@requer_tipo(1)
def dashboard_admin(request):
    return render(
        request,
        'laboratorio/dashboard/admin/dashboard_admin.html'
    )


@requer_tipo(2)
def dashboard_colaborador(request):
    return render(
        request,
        'laboratorio/dashboard/colaborador/dashboard_colaborador.html'
    )


@requer_tipo(3)
def dashboard_cliente(request):
    return render(
        request,
        'laboratorio/dashboard/cliente/dashboard_cliente.html'
    )


@requer_tipo(1)
def encomendas_admin(request):
    return render(
        request,
        'laboratorio/dashboard/admin/encomendas.html'
    )


def logout(request):
    request.session.flush()
    return redirect('entrar')


@requer_tipo(1)
def utilizadores_admin(request):

    tipo_atual = request.GET.get('tipo', 'clientes')
    pesquisa = request.GET.get('pesquisa', '').strip()

    erro_formulario = None
    abrir_modal = None
    dados_formulario = {}

    # ==========================================
    # CRIAR UTILIZADOR
    # ==========================================

    if request.method == 'POST':

        tipo = request.POST.get('tipo_utilizador', '').strip()

        dados_formulario = {
            'nome': request.POST.get('nome', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'telefone': request.POST.get('telefone', '').strip(),
            'nif': request.POST.get('nif', '').strip(),
            'morada': request.POST.get('morada', '').strip(),
        }

        if tipo not in ('cliente', 'colaborador'):
            messages.error(request, 'Tipo de utilizador inválido.')
            return redirect('utilizadores_admin')

        abrir_modal = tipo
        tipo_atual = 'clientes' if tipo == 'cliente' else 'colaboradores'

        try:
            # A API valida os dados e cria utilizador (+ cliente e morada)
            # numa só transação.
            api(
                'POST', '/utilizadores/admin', request,
                json={'tipo': tipo, **dados_formulario}
            )

            messages.success(request, 'Utilizador criado com sucesso!')

            return redirect(
                f'/dashboard/admin/utilizadores/?tipo={tipo_atual}'
            )

        except ApiError as erro:
            if erro.status == 401:
                return sessao_expirada(request)
            erro_formulario = erro.detalhe

    # ==========================================
    # CONSULTAR UTILIZADORES (via API)
    # ==========================================

    painel = {
        'tipo': 'colaboradores' if tipo_atual == 'colaboradores' else 'clientes',
        'total_clientes': 0,
        'total_colaboradores': 0,
        'utilizadores': [],
    }

    try:
        painel = api(
            'GET', '/utilizadores/painel', request,
            params={'tipo': tipo_atual, 'pesquisa': pesquisa}
        )
    except ApiError as erro:
        if erro.status == 401:
            return sessao_expirada(request)
        messages.error(request, erro.detalhe)

    return render(
        request,
        'laboratorio/dashboard/admin/utilizadores.html',
        {
            'tipo_atual': painel['tipo'],
            'pesquisa': pesquisa,
            'utilizadores': painel['utilizadores'],
            'total_clientes': painel['total_clientes'],
            'total_colaboradores': painel['total_colaboradores'],

            # Dados dos formulários
            'erro_formulario': erro_formulario,
            'abrir_modal': abrir_modal,
            'dados_formulario': dados_formulario,
        }
    )
