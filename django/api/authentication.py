from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from laboratorio.database.utilizador import obter_utilizador


class UtilizadorSessao:

    def __init__(self, id, tipo_utilizador, estado):
        self.id = id
        self.tipo_utilizador = tipo_utilizador
        self.estado = estado
        self.is_authenticated = True


class AutenticacaoSessao(BaseAuthentication):

    def authenticate(self, request):
        utilizador_id = request.session.get('utilizador_id')

        if not utilizador_id:
            return None

        utilizador = obter_utilizador(utilizador_id)

        if utilizador is None:
            raise AuthenticationFailed('Utilizador não encontrado.')

        tipo_utilizador = utilizador[6]
        estado = utilizador[7]

        if estado not in [2, 12]:
            raise AuthenticationFailed(
                'A tua conta não está autorizada a aceder à API.'
            )

        return (
            UtilizadorSessao(
                utilizador[0],
                tipo_utilizador,
                estado
            ),
            None
        )
