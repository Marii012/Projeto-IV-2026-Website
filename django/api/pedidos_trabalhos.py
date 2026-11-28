from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from laboratorio.database.pedido_trabalho import (
    listar_pedidos_trabalho,
    obter_pedido_trabalho,
    listar_pedidos_trabalho_cliente,
    obter_pedido_trabalho_cliente,
    assumir_etapa,
    colocar_em_espera,
    colocar_em_prova,
    finalizar_etapa,
    concluir_trabalho 
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar(request):
    if request.user.tipo_utilizador == 3:
        trabalhos = listar_pedidos_trabalho_cliente(request.user.id)
    else:
        trabalhos = listar_pedidos_trabalho()

    resultado = []

    for trabalho in trabalhos:
        resultado.append({
            'id': trabalho[0],
            'e_digital': trabalho[1],
            'material_da_clinica': trabalho[2],
            'material_desc': trabalho[3],
            'material_qtd': trabalho[4],
            'material_obs': trabalho[5],
            'cor': trabalho[6],
            'dentes': trabalho[7],
            'data_proxima_consulta': trabalho[8],
            'id_encomenda': trabalho[9],
            'id_tipo_trabalho': trabalho[10],
            'id_estado': trabalho[11],
            'id_material': trabalho[12]
        })

    return Response(resultado)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obter(request, id):
    if request.user.tipo_utilizador == 3:
        trabalho = obter_pedido_trabalho_cliente(id, request.user.id)
    else:
        trabalho = obter_pedido_trabalho(id)

    if trabalho is None:
        raise Http404('Trabalho não encontrado.')

    resultado = {
        'id': trabalho[0],
        'e_digital': trabalho[1],
        'material_da_clinica': trabalho[2],
        'material_desc': trabalho[3],
        'material_qtd': trabalho[4],
        'material_obs': trabalho[5],
        'cor': trabalho[6],
        'dentes': trabalho[7],
        'data_proxima_consulta': trabalho[8],
        'id_encomenda': trabalho[9],
        'id_tipo_trabalho': trabalho[10],
        'id_estado': trabalho[11],
        'id_material': trabalho[12]
    }

    return Response(resultado)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assumir(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para assumir etapas.'},
            status=403
        )

    id_etapa = request.data.get('id_etapa')

    if not id_etapa:
        return Response(
            {'erro': 'É necessário indicar a etapa.'},
            status=400
        )

    try:
        id_execucao = assumir_etapa(
            id,
            id_etapa,
            request.user.id
        )

        return Response({
            'mensagem': 'Etapa assumida com sucesso.',
            'id_execucao': id_execucao
        })

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)

    return Response(resultado)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def espera(request, id):

    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para colocar trabalhos em espera.'},
            status=403
        )

    motivo = request.data.get('motivo')

    if not motivo:
        return Response(
            {'erro': 'É necessário indicar o motivo da espera.'},
            status=400
        )

    try:
        colocar_em_espera(id, motivo, request.user.id)

        return Response({
            'mensagem': 'Trabalho colocado em espera com sucesso.'
        })

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prova(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    try:
        colocar_em_prova(id, request.user.id)
        return Response({'mensagem': 'Trabalho colocado em prova com sucesso.'})
    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finalizar(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    try:
        finalizar_etapa(id, request.user.id)
        return Response({'mensagem': 'Etapa finalizada com sucesso.'})
    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def concluir(request, id):
    if request.user.tipo_utilizador not in [1, 2]:
        return Response(
            {'erro': 'Não tens permissões para realizar esta operação.'},
            status=403
        )

    try:
        concluir_trabalho(id, request.user.id)
        return Response({'mensagem': 'Trabalho concluído com sucesso.'})
    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)