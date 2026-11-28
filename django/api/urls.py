from django.urls import path
from . import utilizadores
from . import clientes
from . import encomendas
from . import moradas
from . import pedidos_trabalhos
from . import solicitacoes
from . import execucoes_etapa

urlpatterns = [
    # Utilizadores
    path('utilizadores/', utilizadores.listar, name='api_utilizadores'),
    path('utilizadores/<int:id>/', utilizadores.obter, name='api_obter_utilizador'),
    path('utilizadores/criar/', utilizadores.criar, name='api_criar_utilizador'),
    path('utilizadores/<int:id>/atualizar/', utilizadores.atualizar, name='api_atualizar_utilizador'),
    path('utilizadores/<int:id>/eliminar/', utilizadores.eliminar, name='api_eliminar_utilizador'),

    # Clientes
    path('clientes/', clientes.listar, name='api_clientes'),
    path('clientes/<int:id>/', clientes.obter, name='api_obter_cliente'),
    path('clientes/criar/', clientes.criar, name='api_criar_cliente'),
    path('clientes/<int:id>/atualizar/', clientes.atualizar, name='api_atualizar_cliente'),
    path('clientes/<int:id>/eliminar/', clientes.eliminar, name='api_eliminar_cliente'),

    # Moradas
    path('moradas/', moradas.listar, name='api_moradas'),
    path('moradas/<int:id>/', moradas.obter, name='api_obter_morada'),
    path('moradas/criar/', moradas.criar, name='api_criar_morada'),
    path('moradas/<int:id>/atualizar/', moradas.atualizar, name='api_atualizar_morada'),
    path('moradas/<int:id>/eliminar/', moradas.eliminar, name='api_eliminar_morada'),

    # Encomendas
    path('encomendas/', encomendas.listar, name='api_encomendas'),
    path('encomendas/<int:id>/', encomendas.obter, name='api_obter_encomenda'),
    path('encomendas/criar/', encomendas.criar, name='api_criar_encomenda'),
    path('encomendas/<int:id>/recusar/', encomendas.recusar, name='api_recusar_encomenda'),
    path('encomendas/<int:id>/entregar/', encomendas.entregar, name='api_entregar_encomenda'),

    # Pedido de Trabalho
    path('trabalhos/', pedidos_trabalhos.listar, name='api_trabalhos'),
    path('trabalhos/<int:id>/', pedidos_trabalhos.obter, name='api_obter_trabalho'),
    path('trabalhos/<int:id>/assumir/', pedidos_trabalhos.assumir, name='api_assumir_etapa'),
    path('encomendas/<int:id>/autorizar/', encomendas.autorizar, name='api_autorizar_encomenda'),
    path('trabalhos/<int:id>/espera/', pedidos_trabalhos.espera, name='api_trabalho_espera'),
    path('trabalhos/<int:id>/prova/', pedidos_trabalhos.prova, name='api_trabalho_prova'),
    path('execucoes/<int:id>/finalizar/', pedidos_trabalhos.finalizar, name='api_finalizar_etapa'),
    path('trabalhos/<int:id>/concluir/', pedidos_trabalhos.concluir, name='api_concluir_trabalho'),

    # Solicitações
    path('solicitacoes/', solicitacoes.listar, name='api_solicitacoes'),
    path('solicitacoes/<int:id>/', solicitacoes.obter, name='api_obter_solicitacao'),
    path('solicitacoes/criar/', solicitacoes.criar, name='api_criar_solicitacao'),
    path('solicitacoes/<int:id>/decidir/', solicitacoes.decidir, name='api_decidir_solicitacao'),

    # Execuções de Etapas
    path('execucoes/', execucoes_etapa.listar, name='api_execucoes'),
    path('execucoes/<int:id>/', execucoes_etapa.obter, name='api_obter_execucao'),
    path('execucoes/<int:id>/encaminhar/', execucoes_etapa.encaminhar, name='api_encaminhar_etapa'),
]
