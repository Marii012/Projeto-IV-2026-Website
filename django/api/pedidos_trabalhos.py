from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from api.permissions import AdministradorOuColaborador
from laboratorio.database.pedido_trabalho import (
    listar_pedidos_trabalho,
    obter_pedido_trabalho,
    listar_pedidos_trabalho_cliente,
    obter_pedido_trabalho_cliente
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
