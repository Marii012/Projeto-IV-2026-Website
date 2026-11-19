from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('encomendas', views.encomendas_api),
]