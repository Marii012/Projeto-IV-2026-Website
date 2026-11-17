
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'laboratorio/public/home.html')


def contacto(request):
    return redirect('/#contactos')


def entrar(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        utilizador = authenticate(
            request,
            username=username,
            password=password
        )

        if utilizador is not None:
            login(request, utilizador)
            return redirect('dashboard')

        messages.error(request, 'Utilizador ou palavra-passe inválidos.')

    return render(request, 'laboratorio/auth/login.html')


def registo(request):
    return render(request, 'laboratorio/auth/registo.html')


def dashboard(request):
    return render(request, 'laboratorio/dashboard.html')

