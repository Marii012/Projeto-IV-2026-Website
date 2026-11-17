from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from laboratorio.database.utilizador import obter_utilizador_por_email


def home(request):
    return render(request, 'laboratorio/public/home.html')


def contacto(request):
    return redirect('/#contactos')


def entrar(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        utilizador = obter_utilizador_por_email(email)

        if utilizador is None:
            messages.error(
                request,
                'Email ou palavra-passe inválidos.'
            )
            return render(request, 'laboratorio/auth/login.html')

        # Estrutura devolvida pela consulta SQL:
        # 0 = id
        # 1 = nome
        # 2 = email
        # 3 = password_hash
        # 4 = cargo
        # 5 = data_registo
        # 6 = id_tipo_utilizador
        # 7 = id_estado

        password_hash = utilizador[3]

        if not check_password(password, password_hash):
            messages.error(
                request,
                'Email ou palavra-passe inválidos.'
            )
            return render(request, 'laboratorio/auth/login.html')

        # Guardar dados do utilizador na sessão
        request.session['utilizador_id'] = utilizador[0]
        request.session['utilizador_nome'] = utilizador[1]
        request.session['utilizador_email'] = utilizador[2]
        request.session['tipo_utilizador_id'] = utilizador[6]

        # Encaminhar conforme o tipo de utilizador
        tipo = utilizador[6]

        if tipo == 1:
            return redirect('dashboard_admin')

        elif tipo == 2:
            return redirect('dashboard_colaborador')

        elif tipo == 3:
            return redirect('dashboard_cliente')

        messages.error(
            request,
            'Tipo de utilizador não reconhecido.'
        )
        return render(request, 'laboratorio/auth/login.html')

    return render(request, 'laboratorio/auth/login.html')


def registo(request):
    return render(request, 'laboratorio/auth/registo.html')


def dashboard_admin(request):
    return render(
        request,
        'laboratorio/dashboard/admin/dashboard_admin.html'
    )


def dashboard_colaborador(request):
    return render(
        request,
        'laboratorio/dashboard/colaborador/dashboard_colaborador.html'
    )


def dashboard_cliente(request):
    return render(
        request,
        'laboratorio/dashboard/cliente/dashboard_cliente.html'
    )