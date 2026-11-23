from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404

from rest_framework.permissions import IsAuthenticated
from api.permissions import ApenasAdministrador
from rest_framework.decorators import permission_classes

from laboratorio.database.utilizador import listar_utilizadores
from laboratorio.database.utilizador import obter_utilizador
from laboratorio.database.utilizador import inserir_utilizador
from laboratorio.database.utilizador import atualizar_utilizador
from laboratorio.database.utilizador import eliminar_utilizador
from laboratorio.database.utilizador import obter_utilizador_por_email


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def listar(request):

    dados = listar_utilizadores()

    utilizadores = []

    for utilizador in dados:
        utilizadores.append({
            'id': utilizador[0],
            'nome': utilizador[1],
            'email': utilizador[2],
            'cargo': utilizador[4],
            'data_registo': utilizador[5],
            'id_tipo_utilizador': utilizador[6],
            'id_estado': utilizador[7]
        })

    return Response({
        'utilizadores': utilizadores
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def obter(request, id):

    utilizador = obter_utilizador(id)

    if utilizador is None:
        raise Http404("Utilizador não encontrado.")

    dados = {
        'id': utilizador[0],
        'nome': utilizador[1],
        'email': utilizador[2],
        'cargo': utilizador[4],
        'data_registo': utilizador[5],
        'id_tipo_utilizador': utilizador[6],
        'id_estado': utilizador[7]
    }

    return Response(dados)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def criar(request):

    dados = request.data

    try:
        email = dados['email']

        utilizador_existente = obter_utilizador_por_email(email)

        if utilizador_existente is not None:
            return Response({
                'erro': 'Já existe um utilizador registado com este email.'
            }, status=400)

        id = inserir_utilizador(
            dados['nome'],
            email,
            dados['password'],
            dados.get('cargo'),
            dados['id_tipo_utilizador'],
            dados['id_estado']
        )

        return Response({
            'mensagem': 'Utilizador criado com sucesso.',
            'id': id
        }, status=201)

    except KeyError as erro:
        return Response({
            'erro': f'Campo obrigatório em falta: {erro}'
        }, status=400)

    except ValueError as erro:
        return Response({
            'erro': str(erro)
        }, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def atualizar(request, id):

    dados = request.data

    try:
        email = dados['email']

        utilizador_existente = obter_utilizador_por_email(email)

        if utilizador_existente is not None and utilizador_existente[0] != id:
            return Response({
                'erro': 'Este email já está associado a outro utilizador.'
            }, status=400)

        resultado = atualizar_utilizador(
            id,
            dados['nome'],
            email,
            dados.get('password'),
            dados.get('cargo'),
            dados['id_tipo_utilizador'],
            dados['id_estado']
        )

        if resultado == 0:
            return Response({
                'erro': 'Utilizador não encontrado.'
            }, status=404)

        return Response({
            'mensagem': 'Utilizador atualizado com sucesso.'
        }, status=200)

    except KeyError as erro:
        return Response({
            'erro': f'Campo obrigatório em falta: {erro}'
        }, status=400)

    except ValueError as erro:
        return Response({
            'erro': str(erro)
        }, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def eliminar(request, id):

    resultado = eliminar_utilizador(id)

    if resultado == 0:
        return Response({
            'erro': 'Utilizador não encontrado.'
        }, status=404)

    return Response({
        'mensagem': 'Utilizador eliminado com sucesso.'
    }, status=200)
