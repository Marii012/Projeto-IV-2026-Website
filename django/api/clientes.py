
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from api.permissions import ApenasAdministrador

from laboratorio.database.cliente import listar_clientes
from laboratorio.database.cliente import obter_cliente
from laboratorio.database.cliente import inserir_cliente
from laboratorio.database.cliente import atualizar_cliente
from laboratorio.database.cliente import eliminar_cliente
from laboratorio.database.utilizador import obter_utilizador


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def listar(request):

    dados = listar_clientes()

    clientes = []

    for cliente in dados:
        clientes.append({
            'id': cliente[0],
            'nome': cliente[1],
            'nif': cliente[2],
            'telefone': cliente[3],
            'data_aprovacao': cliente[4],
            'id_utilizador': cliente[5]
        })

    return Response({
        'clientes': clientes
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def obter(request, id):

    cliente = obter_cliente(id)

    if cliente is None:
        raise Http404("Cliente não encontrado.")

    dados = {
        'id': cliente[0],
        'nome': cliente[1],
        'nif': cliente[2],
        'telefone': cliente[3],
        'data_aprovacao': cliente[4],
        'id_utilizador': cliente[5]
    }

    return Response(dados)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def criar(request):

    dados = request.data

    try:

        utilizador = obter_utilizador(dados['id_utilizador'])

        if utilizador is None:
            return Response({
                'erro': 'Utilizador não encontrado.'
            }, status=404)
        
        id = inserir_cliente(
            dados['nome'],
            dados['nif'],
            dados.get('telefone'),
            dados.get('data_aprovacao'),
            dados['id_utilizador']
        )

        return Response({
            'mensagem': 'Cliente criado com sucesso.',
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
        utilizador = obter_utilizador(dados['id_utilizador'])

        if utilizador is None:
            return Response({
                'erro': 'Utilizador não encontrado.'
            }, status=404)
        
        resultado = atualizar_cliente(
            id,
            dados['nome'],
            dados['nif'],
            dados.get('telefone'),
            dados.get('data_aprovacao'),
            dados['id_utilizador']
        )

        if resultado == 0:
            return Response({
                'erro': 'Cliente não encontrado.'
            }, status=404)

        return Response({
            'mensagem': 'Cliente atualizado com sucesso.'
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

    resultado = eliminar_cliente(id)

    if resultado == 0:
        return Response({
            'erro': 'Cliente não encontrado.'
        }, status=404)

    return Response({
        'mensagem': 'Cliente eliminado com sucesso.'
    }, status=200)
