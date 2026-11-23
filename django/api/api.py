from rest_framework.decorators import api_view
from rest_framework.response import Response
from laboratorio.database.utilizador import listar_utilizadores


@api_view(['GET'])
def utilizadores(request):
    utilizadores = listar_utilizadores()
    return Response({
        'utilizadores': utilizadores
    })