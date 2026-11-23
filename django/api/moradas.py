from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from api.permissions import ApenasAdministrador

from laboratorio.database.morada import listar_moradas
from laboratorio.database.morada import obter_morada
from laboratorio.database.morada import inserir_morada
from laboratorio.database.morada import atualizar_morada
from laboratorio.database.morada import eliminar_morada

from laboratorio.database.cliente import obter_cliente


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def listar(request):

    dados = listar_moradas()

    moradas = []

    for morada in dados:
        moradas.append({
            'id': morada[0],
            'nome_clinica': morada[1],
            'morada': morada[2],
            'id_cliente': morada[3]
        })

    return Response({
        'moradas': moradas
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def obter(request, id):

    morada = obter_morada(id)

    if morada is None:
        raise Http404("Morada não encontrada.")

    dados = {
        'id': morada[0],
        'nome_clinica': morada[1],
        'morada': morada[2],
        'id_cliente': morada[3]
    }

    return Response(dados)



@api_view(['POST'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def criar(request):

    dados = request.data

    try:

        cliente = obter_cliente(dados['id_cliente'])

        if cliente is None:
            return Response({
                'erro': 'Cliente não encontrado.'
            }, status=404)

        id = inserir_morada(
            dados['nome_clinica'],
            dados['morada'],
            dados['id_cliente']
        )

        return Response({
            'mensagem': 'Morada criada com sucesso.',
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

        cliente = obter_cliente(dados['id_cliente'])

        if cliente is None:
            return Response({
                'erro': 'Cliente não encontrado.'
            }, status=404)

        resultado = atualizar_morada(
            id,
            dados['nome_clinica'],
            dados['morada'],
            dados['id_cliente']
        )

        if resultado == 0:
            return Response({
                'erro': 'Morada não encontrada.'
            }, status=404)

        return Response({
            'mensagem': 'Morada atualizada com sucesso.'
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

    resultado = eliminar_morada(id)

    if resultado == 0:
        return Response({
            'erro': 'Morada não encontrada.'
        }, status=404)

    return Response({
        'mensagem': 'Morada eliminada com sucesso.'
    }, status=200)

