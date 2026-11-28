from django.urls import include, path
from laboratorio import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacto/', views.contacto, name='contacto'),
    path('entrar/', views.entrar, name='entrar'),
    path('registo/', views.registo, name='registo'),

    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/colaborador/', views.dashboard_colaborador, name='dashboard_colaborador'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),

    path('dashboard/admin/utilizadores/', views.utilizadores_admin, name='utilizadores_admin'),
    path('dashboard/admin/encomendas/', views.encomendas_admin, name='encomendas_admin'),

    path('logout/', views.logout, name='logout'),
    path('api/', include('api.urls')),
]
