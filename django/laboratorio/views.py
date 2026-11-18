from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from laboratorio.database.utilizador import obter_utilizador_por_email

from django.db import connection, transaction, IntegrityError
from laboratorio.database.utilizador import (
    inserir_utilizador,
    inserir_cliente,
    inserir_morada,
)


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

def utilizadores_admin(request):
    return render(
        request,
        'laboratorio/dashboard/admin/utilizadores.html'
    )


def encomendas_admin(request):
    return render(
        request,
        'laboratorio/dashboard/admin/encomendas.html'
    )

def logout(request):
    request.session.flush()
    return redirect('entrar')


def utilizadores_admin(request):

    tipo_atual = request.GET.get('tipo', 'clientes')
    pesquisa = request.GET.get('pesquisa', '').strip()

    erro_formulario = None
    abrir_modal = None
    dados_formulario = {}

    # ==========================================
    # CRIAR UTILIZADOR
    # ==========================================

    if request.method == 'POST':

        tipo = request.POST.get('tipo_utilizador', '').strip()
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()

        dados_formulario = {
            'nome': nome,
            'email': email,
            'telefone': request.POST.get('telefone', '').strip(),
            'nif': request.POST.get('nif', '').strip(),
            'morada': request.POST.get('morada', '').strip(),
        }

        if tipo not in ('cliente', 'colaborador'):

            messages.error(request, 'Tipo de utilizador inválido.')
            return redirect('utilizadores_admin')

        abrir_modal = tipo

        if tipo == 'cliente':
            tipo_atual = 'clientes'
            id_tipo_utilizador = 3
        else:
            tipo_atual = 'colaboradores'
            id_tipo_utilizador = 2

        # Estado ativo
        id_estado = 12

        try:

            # Validar campos obrigatórios
            if not nome or not email:
                raise ValueError(
                    'Preenche todos os campos obrigatórios.'
                )

            # Validar dados do cliente
            if tipo == 'cliente':

                nif = dados_formulario['nif']
                telefone = dados_formulario['telefone']
                morada = dados_formulario['morada']

                if not nif or not telefone or not morada:
                    raise ValueError(
                        'Preenche o NIF, telefone e morada.'
                    )

                if not nif.isdigit() or len(nif) != 9:
                    raise ValueError(
                        'O NIF deve conter exatamente 9 algarismos.'
                    )

            # Criar registos na base de dados
            with transaction.atomic():

                id_utilizador = inserir_utilizador(
                    nome=nome,
                    email=email,
                    password=None,
                    cargo=None,
                    id_tipo_utilizador=id_tipo_utilizador,
                    id_estado=id_estado
                )

                # Criar cliente e morada
                if tipo == 'cliente':

                    id_cliente = inserir_cliente(
                        id_utilizador=id_utilizador,
                        nome=nome,
                        nif=nif,
                        telefone=telefone
                    )

                    inserir_morada(
                        id_cliente=id_cliente,
                        nome_clinica=nome,
                        morada=morada
                    )

            # Sucesso
            messages.success(
                request,
                'Utilizador criado com sucesso!'
            )

            return redirect(
                f'/dashboard/admin/utilizadores/?tipo={tipo_atual}'
            )

        # ==========================================
        # TRATAMENTO DE ERROS DA BASE DE DADOS
        # ==========================================

        except IntegrityError as erro:

            print("ERRO DE BASE DE DADOS:", repr(erro))

            erro_bd = str(erro)

            if 'utilizador_email_key' in erro_bd:

                erro_formulario = (
                    'O e-mail introduzido já está associado '
                    'a outra conta. Escolhe outro e-mail.'
                )

            elif 'cliente_nif_key' in erro_bd:

                erro_formulario = (
                    'O NIF introduzido já está associado '
                    'a outro cliente.'
                )

            elif 'cliente_id_utilizador_key' in erro_bd:

                erro_formulario = (
                    'Este utilizador já tem um registo de cliente.'
                )

            elif 'utilizador' in erro_bd and 'unique' in erro_bd.lower():

                erro_formulario = (
                    'Já existe uma conta com estes dados.'
                )

            else:

                erro_formulario = (
                    'Não foi possível guardar os dados. '
                    'Verifica os campos e tenta novamente.'
                )

        # ==========================================
        # ERROS DE VALIDAÇÃO
        # ==========================================

        except ValueError as erro:

            erro_formulario = str(erro)

        # ==========================================
        # OUTROS ERROS
        # ==========================================

        except Exception as erro:

            print("ERRO INESPERADO:", repr(erro))

            erro_formulario = (
                'Ocorreu um problema ao criar a conta. '
                'Tenta novamente.'
            )

    # ==========================================
    # DEFINIR UTILIZADORES A LISTAR
    # ==========================================

    if tipo_atual == 'colaboradores':
        id_tipo = 2
    else:
        tipo_atual = 'clientes'
        id_tipo = 3

    # ==========================================
    # CONSULTAR BASE DE DADOS
    # ==========================================

    with connection.cursor() as cursor:

        # Total de clientes
        cursor.execute("""
            SELECT COUNT(*)
            FROM utilizador
            WHERE id_tipo_utilizador = 3
        """)

        total_clientes = cursor.fetchone()[0]

        # Total de colaboradores
        cursor.execute("""
            SELECT COUNT(*)
            FROM utilizador
            WHERE id_tipo_utilizador = 2
        """)

        total_colaboradores = cursor.fetchone()[0]

        # Consultar utilizadores
        sql = """
            SELECT
                u.id,
                u.nome,
                u.email,
                e.descricao AS estado,
                c.nif,
                0 AS total_trabalhos
            FROM utilizador u
            LEFT JOIN cliente c
                ON c.id_utilizador = u.id
            LEFT JOIN estado e
                ON e.id = u.id_estado
            WHERE u.id_tipo_utilizador = %s
        """

        parametros = [id_tipo]

        # Pesquisa por nome, email ou NIF
        if pesquisa:

            sql += """
                AND (
                    u.nome ILIKE %s
                    OR u.email ILIKE %s
                    OR CAST(c.nif AS TEXT) ILIKE %s
                )
            """

            pesquisa_sql = f'%{pesquisa}%'

            parametros.extend([
                pesquisa_sql,
                pesquisa_sql,
                pesquisa_sql
            ])

        sql += " ORDER BY u.nome ASC"

        cursor.execute(sql, parametros)

        colunas = [
            coluna[0]
            for coluna in cursor.description
        ]

        utilizadores = [
            dict(zip(colunas, linha))
            for linha in cursor.fetchall()
        ]

    # ==========================================
    # APRESENTAR PÁGINA
    # ==========================================

    return render(
        request,
        'laboratorio/dashboard/admin/utilizadores.html',
        {
            'tipo_atual': tipo_atual,
            'pesquisa': pesquisa,
            'utilizadores': utilizadores,
            'total_clientes': total_clientes,
            'total_colaboradores': total_colaboradores,

            # Dados dos formulários
            'erro_formulario': erro_formulario,
            'abrir_modal': abrir_modal,
            'dados_formulario': dados_formulario,
        }
    )
