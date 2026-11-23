from rest_framework.permissions import BasePermission


class ApenasAdministrador(BasePermission):

    message = 'Não tens permissões para realizar esta operação.'

    def has_permission(self, request, view):

        utilizador = request.user

        if not utilizador or not utilizador.is_authenticated:
            return False

        return utilizador.tipo_utilizador == 1

class AdministradorOuColaborador(BasePermission):
    message = 'Não tens permissões para realizar esta operação.'

    def has_permission(self, request, view):
        utilizador = request.user

        if not utilizador or not utilizador.is_authenticated:
            return False

        return utilizador.tipo_utilizador in [1, 2]
