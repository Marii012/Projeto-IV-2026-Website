"""Cliente HTTP da API do laboratório.

O Django já não fala com a base de dados: tudo passa por esta API.
"""
import requests
from django.conf import settings


class ApiError(Exception):
    """Erro devolvido pela API (ou impossibilidade de a contactar)."""

    def __init__(self, status, detalhe):
        super().__init__(detalhe)
        self.status = status
        self.detalhe = detalhe


def api(metodo, caminho, request=None, **kwargs):
    """Faz um pedido à API e devolve o JSON (ou None se não houver corpo).

    - Se `request` for dado, encaminha o cookie da sessão para a API Django.
    - Em caso de erro levanta ApiError(status, detalhe) com a mensagem da API.
    """
    headers = kwargs.pop('headers', {})
    if request is not None:
        cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if cookie:
            headers['Cookie'] = f'{settings.SESSION_COOKIE_NAME}={cookie}'

    url = settings.API_URL.rstrip('/') + caminho
    try:
        resposta = requests.request(
            metodo, url, headers=headers, timeout=settings.API_TIMEOUT, **kwargs
        )
    except requests.RequestException as erro:
        print('ERRO AO CONTACTAR A API:', repr(erro))
        raise ApiError(
            503, 'Não foi possível contactar o servidor. Tenta novamente mais tarde.'
        )

    if resposta.status_code >= 400:
        try:
            detalhe = resposta.json().get('detail')
        except (ValueError, AttributeError):
            detalhe = None
        if not isinstance(detalhe, str):
            detalhe = 'Ocorreu um erro ao comunicar com o servidor.'
        raise ApiError(resposta.status_code, detalhe)

    if resposta.status_code == 204 or not resposta.content:
        return None
    return resposta.json()
