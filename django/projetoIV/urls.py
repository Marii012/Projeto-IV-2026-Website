from django.contrib import admin
from django.urls import path
from laboratorio import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('contacto/', views.contacto, name='contacto'),
    path('entrar/', views.entrar, name='entrar'),
    path('registo/', views.registo, name='registo'),

    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/colaborador/', views.dashboard_colaborador, name='dashboard_colaborador'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
]
