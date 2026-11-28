from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.db import transaction

from laboratorio.database.pedido_trabalho import inserir_pedido_trabalho
from api.permissions import ApenasAdministrador, AdministradorOuColaborador
from laboratorio.database.encomenda import (
    listar_encomendas,
    obter_encomenda,
    criar_encomenda,
    recusar_encomenda,
    entregar_encomenda,
    autorizar_encomenda
)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador, AdministradorOuColaborador])
def listar(request):
    encomendas = listar_encomendas()

    resultado = []

    for encomenda in encomendas:
        resultado.append({
            'id': encomenda[0],
            'cliente_nome_avulso': encomenda[1],
            'morada_avulsa': encomenda[2],
            'medico_nome': encomenda[3],
            'paciente_idade': encomenda[4],
            'observacoes_cliente': encomenda[5],
            'motivo_standby': encomenda[6],
            'data_criacao': encomenda[7],
            'data_aceitacao': encomenda[8],
            'prazo_dias_uteis': encomenda[9],
            'data_limite': encomenda[10],
            'data_finalizacao': encomenda[11],
            'id_cliente': encomenda[12],
            'id_paciente': encomenda[13],
            'id_criado_por': encomenda[14],
            'id_aceite_por': encomenda[15],
            'id_estado': encomenda[16],
            'id_encomenda_origem': encomenda[17]
        })

    return Response(resultado)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ApenasAdministrador, AdministradorOuColaborador])
def obter(request, id):
    encomenda = obter_encomenda(id)

    if encomenda is None:
        raise Http404('Encomenda não encontrada.')

    resultado = {
        'id': encomenda[0],
        'cliente_nome_avulso': encomenda[1],
        'morada_avulsa': encomenda[2],
        'medico_nome': encomenda[3],
        'paciente_idade': encomenda[4],
        'observacoes_cliente': encomenda[5],
        'motivo_standby': encomenda[6],
        'data_criacao': encomenda[7],
        'data_aceitacao': encomenda[8],
        'prazo_dias_uteis': encomenda[9],
        'data_limite': encomenda[10],
        'data_finalizacao': encomenda[11],
        'id_cliente': encomenda[12],
        'id_paciente': encomenda[13],
        'id_criado_por': encomenda[14],
        'id_aceite_por': encomenda[15],
        'id_estado': encomenda[16],
        'id_encomenda_origem': encomenda[17]
    }

    return Response(resultado)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar(request):
    dados = request.data

    try:
        trabalhos = dados['trabalhos']

        if not isinstance(trabalhos, list) or not trabalhos:
            raise ValueError('Adiciona pelo menos um trabalho à encomenda.')

        with transaction.atomic():

            id_encomenda = criar_encomenda(
                request.user.id,
                dados['id_cliente'],
                dados.get('cliente_nome_avulso'),
                dados.get('morada_avulsa'),
                dados['medico_nome'],
                dados['paciente_identificador'],
                dados['paciente_sexo'],
                dados['paciente_idade'],
                dados.get('observacoes')
            )

            for trabalho in trabalhos:
                inserir_pedido_trabalho(
                    trabalho.get('e_digital'),
                    trabalho.get('material_da_clinica'),
                    trabalho.get('material_desc'),
                    trabalho.get('material_qtd'),
                    trabalho.get('material_obs'),
                    trabalho.get('cor'),
                    trabalho.get('dentes'),
                    trabalho.get('data_proxima_consulta'),
                    id_encomenda,
                    trabalho['id_tipo_trabalho'],
                    4,
                    trabalho.get('id_material')
                )

        return Response({
            'mensagem': 'Encomenda criada com sucesso.',
            'id': id_encomenda
        }, status=201)

    except KeyError as erro:
        return Response({
            'erro': f'O campo {erro.args[0]} é obrigatório.'
        }, status=400)

    except ValueError as erro:
        return Response({
            'erro': str(erro)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def recusar(request, id):
    try:
        recusar_encomenda(id, request.user.id)

        return Response({
            'mensagem': 'Encomenda recusada com sucesso.'
        })

    except Exception:
        return Response({
            'erro': 'Não foi possível recusar a encomenda. Verifica se existe e se está em avaliação.'
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ApenasAdministrador])
def entregar(request, id):
    try:
        entregar_encomenda(id, request.user.id)

        return Response({
            'mensagem': 'Encomenda entregue com sucesso.'
        })

    except Exception:
        return Response({
            'erro': 'Não foi possível entregar a encomenda. Verifica se existe e se está concluída.'
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def autorizar(request, id):
    if request.user.tipo_utilizador != 1:
        return Response(
            {'erro': 'Apenas o administrador pode autorizar encomendas.'},
            status=403
        )

    try:
        autorizar_encomenda(id, request.user.id)

        return Response({
            'mensagem': 'Encomenda autorizada com sucesso.'
        })

    except ValueError as erro:
        return Response({'erro': str(erro)}, status=400)

    except Exception as erro:
        return Response({'erro': str(erro)}, status=400)