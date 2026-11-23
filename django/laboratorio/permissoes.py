"""Controlo de acesso às páginas (a segurança dos dados está na API)."""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

DASHBOARD_POR_TIPO = {
    1: 'dashboard_admin',
    2: 'dashboard_colaborador',
    3: 'dashboard_cliente',
}


def sessao_expirada(request):
    request.session.flush()
    messages.error(request, 'A tua sessão expirou. Entra novamente.')
    return redirect('entrar')


def requer_tipo(*tipos):
    """Só deixa entrar utilizadores autenticados de um dos tipos indicados."""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('token'):
                return redirect('entrar')
            tipo = request.session.get('tipo_utilizador_id')
            if tipo not in tipos:
                return redirect(DASHBOARD_POR_TIPO.get(tipo, 'entrar'))
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
