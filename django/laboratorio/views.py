from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import PedidoContacto


def home(request):
    if request.method == 'POST':
        PedidoContacto.objects.create(
            nome=request.POST.get('nome', '').strip(),
            laboratorio=request.POST.get('laboratorio', '').strip(),
            email=request.POST.get('email', '').strip(),
            telefone=request.POST.get('telefone', '').strip(),
            mensagem=request.POST.get('mensagem', '').strip(),
        )
        messages.success(request, 'Pedido enviado. Obrigado pelo contacto!')
        return redirect('home')
    return render(request, 'laboratorio/home.html')


def contacto(request):
    return redirect('/#contactos')


def entrar(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        utilizador = authenticate(request, username=username, password=password)
        if utilizador is not None:
            login(request, utilizador)
            return redirect('dashboard')
        messages.error(request, 'Utilizador ou palavra-passe inválidos.')
    return render(request, 'laboratorio/login.html')


@login_required
def dashboard(request):
    return render(request, 'laboratorio/dashboard.html', {
        'total_pedidos_contacto': PedidoContacto.objects.count(),
    })
