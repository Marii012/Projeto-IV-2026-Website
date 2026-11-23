from django.urls import path
from . import utilizadores
from . import clientes
from . import encomendas
from . import moradas
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

    #Pedido de Trabalho
    
]
