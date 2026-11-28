from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laboratorio.database.solicitacao import (
    listar_solicitacoes,
    obter_solicitacao,
    listar_solicitacoes_cliente,
    obter_solicitacao_cliente,
    criar_solicitacao,
    decidir_solicitacao
)


# Listar solicitações
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar(request):

    if request.user.tipo_utilizador in [1, 2]:
        solicitacoes = listar_solicitacoes()

    elif request.user.tipo_utilizador == 3:
        solicitacoes = listar_solicitacoes_cliente(request.user.id)

    else:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    dados = []

    for s in solicitacoes:
        dados.append({
            'id': s[0],
            'descricao': s[1],
            'data_pedido': s[2],
            'data_decisao': s[3],
            'id_encomenda': s[4],
            'id_solicitante': s[5],
            'id_decisor': s[6],
            'id_tipo_solicitacao': s[7],
            'id_motivo': s[8],
            'id_estado': s[9]
        })

    return Response(dados)


# Obter solicitação
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obter(request, id):

    if request.user.tipo_utilizador in [1, 2]:
        solicitacao = obter_solicitacao(id)

    elif request.user.tipo_utilizador == 3:
        solicitacao = obter_solicitacao_cliente(id, request.user.id)

    else:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    if solicitacao is None:
        return Response(
            {'erro': 'Solicitação não encontrada.'},
            status=404
        )

    dados = {
        'id': solicitacao[0],
        'descricao': solicitacao[1],
        'data_pedido': solicitacao[2],
        'data_decisao': solicitacao[3],
        'id_encomenda': solicitacao[4],
        'id_solicitante': solicitacao[5],
        'id_decisor': solicitacao[6],
        'id_tipo_solicitacao': solicitacao[7],
        'id_motivo': solicitacao[8],
        'id_estado': solicitacao[9]
    }

    return Response(dados)


# Criar solicitação
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar(request):

    if request.user.tipo_utilizador not in [1, 3]:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    try:
        id_solicitacao = criar_solicitacao(
            request.data.get('id_encomenda'),
            request.user.id,
            request.data.get('id_tipo_solicitacao'),
            request.data.get('id_motivo'),
            request.data.get('descricao'),
            request.data.get('trabalhos', [])
        )

        return Response({
            'mensagem': 'Solicitação criada com sucesso.',
            'id_solicitacao': id_solicitacao
        }, status=201)

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)


# Decidir solicitação
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decidir(request, id):

    if request.user.tipo_utilizador != 1:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    try:
        resultado = decidir_solicitacao(
            id,
            request.user.id,
            request.data.get('aprovar')
        )

        return Response({
            'mensagem': 'Solicitação decidida com sucesso.',
            'resultado': resultado
        })

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)