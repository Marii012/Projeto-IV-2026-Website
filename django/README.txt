PROJETOIV — Django + Bootstrap 5
================================

Este é o ponto de partida Django reconstruído a partir do protótipo Figma Make.
Mantém a identidade visual escura/dourada, tipografia Playfair Display + Outfit,
logótipos fornecidos e as secções principais da página inicial.

REQUISITOS
- Python 3.10+
- PostgreSQL instalado e uma base de dados criada

INSTALAÇÃO (PowerShell, dentro da pasta ProjetoIV_Django)
1) python -m venv venv
2) .\venv\Scripts\Activate.ps1
3) pip install -r requirements.txt

CONFIGURAÇÃO DA BASE DE DADOS
O projeto lê estas variáveis de ambiente (os valores abaixo são exemplos):
$env:DB_NAME = "projeto4"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "A_TUA_PASSWORD"
$env:DB_HOST = "localhost"   # se o servidor for 100.105.58.22, coloca esse IP
$env:DB_PORT = "5432"

Confirma que a base de dados indicada em DB_NAME já existe no pgAdmin 4.
Não coloques a password real em ficheiros que vais partilhar.

EXECUTAR
4) python manage.py makemigrations laboratorio
5) python manage.py migrate
6) python manage.py createsuperuser
7) python manage.py runserver
8) Abrir http://127.0.0.1:8000/

ROTAS DISPONÍVEIS
/             Página pública
/entrar/      Login Django
/dashboard/   Painel (requer autenticação)
/admin/       Administração Django

O formulário de contacto guarda os pedidos na tabela PedidoContacto.
O painel de gestão é uma primeira estrutura; clientes, encomendas, trabalhos,
colaboradores e faturas serão implementados nas próximas etapas, com CRUD SQL.
