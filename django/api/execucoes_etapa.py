from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laboratorio.database.execucao_etapa import (
    listar_execucoes_etapa,
    obter_execucao_etapa,
    encaminhar_etapa
)


# Listar execuções
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar(request):
    if request.user.tipo_utilizador in [1, 2]:
        execucoes = listar_execucoes_etapa()
    else:
        return Response(
            {'erro': 'Não tens permissões para consultar estas execuções.'},
            status=403
        )

    dados = []

    for execucao in execucoes:
        dados.append({
            'id': execucao[0],
            'data_inicio': execucao[1],
            'data_fim': execucao[2],
            'id_pedido_trabalho': execucao[3],
            'id_etapa': execucao[4],
            'id_colaborador': execucao[5]
        })

    return Response(dados)


# Obter execução
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obter(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para consultar estas execuções.'},
            status=403
        )

    execucao = obter_execucao_etapa(id)

    if execucao is None:
        return Response(
            {'erro': 'Execução não encontrada.'},
            status=404
        )

    dados = {
        'id': execucao[0],
        'data_inicio': execucao[1],
        'data_fim': execucao[2],
        'id_pedido_trabalho': execucao[3],
        'id_etapa': execucao[4],
        'id_colaborador': execucao[5]
    }

    return Response(dados)


# Encaminhar etapa
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def encaminhar(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para encaminhar etapas.'},
            status=403
        )

    try:
        resultado = encaminhar_etapa(
            id,
            request.user.id,
            request.data.get('id_proxima_etapa'),
            request.data.get('id_proximo_colaborador'),
            request.data.get('nota'),
            request.data.get('nota_visivel_cliente')
        )

        return Response({
            'mensagem': 'Etapa encaminhada com sucesso.',
            'resultado': resultado
        })

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)

