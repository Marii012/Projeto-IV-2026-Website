from django.contrib import admin
from django.urls import path
from laboratorio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('entrar/', views.entrar, name='entrar'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contacto/', views.contacto, name='contacto'),
]
