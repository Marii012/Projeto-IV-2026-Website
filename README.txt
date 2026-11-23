PROJETO IV - LABORATÓRIO
========================

O projeto tem DOIS serviços. Só a API fala com a base de dados.

    Browser -> Django (site, porta 8000) -> HTTP/JSON -> API (porta 8001) -> PostgreSQL

  api/      API em FastAPI. Único componente com acesso ao PostgreSQL.
  django/   Site (templates + views). NÃO tem base de dados: chama a API.

REQUISITOS
- Python 3.10+
- PostgreSQL com a base de dados já criada (a mesma que já usavam)

1) ARRANCAR A API  (PowerShell, a partir da raiz do projeto)
   cd api
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   copy .env.example .env          # abre o .env e preenche a password da BD e o JWT_SECRET
   uvicorn app.main:app --reload --port 8001

   Documentação interativa (testar endpoints): http://127.0.0.1:8001/docs
   Verificar API + BD:                          http://127.0.0.1:8001/saude
   No /docs: botão "Authorize" -> email em "username" e a password.

2) ARRANCAR O SITE  (outro terminal)
   cd django
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt     # agora precisa de "requests" (já não usa psycopg2)
   python manage.py runserver
   Abrir http://127.0.0.1:8000/

   Se a API estiver noutro endereço:  $env:API_URL = "http://127.0.0.1:8001"

   Já não são precisos "makemigrations", "migrate" nem "createsuperuser".

COMO FUNCIONA O LOGIN
1. O Django envia email + password para POST /auth/login.
2. A API valida (as passwords existentes, geradas pelo Django, continuam a funcionar)
   e devolve um token JWT (válido 8 horas por omissão).
3. O Django guarda o token na sessão e envia-o em cada pedido à API.
4. A API é a única barreira de segurança: verifica o token e o tipo de utilizador
   (1 = administrador, 2 = colaborador, 3 = cliente) em cada endpoint.

ENDPOINTS (lista completa e testável em /docs)
  Autenticação   POST /auth/login | /auth/token | /auth/registo     GET /auth/me
  Utilizadores   /utilizadores (admin)  +  GET /utilizadores/painel  +  POST /utilizadores/admin
  Tabelas        /estados /tipos-utilizador /tipos-ficheiro /tipos-solicitacao
                 /tipos-trabalho /categorias-notificacao /materiais /motivos-solicitacao
                 /etapas /clientes /moradas /pacientes /pedidos-trabalho /execucoes-etapa
                 /notas /ficheiros /solicitacoes /solicitacoes-trabalho /encomendas
                 /notificacoes
                 Cada uma tem: GET (listar), GET /{id}, POST, PATCH /{id}, DELETE /{id}.
                 O PATCH só altera os campos enviados.

QUEM PODE O QUÊ (definido em api/app/routers/tabelas.py)
  Tabelas de apoio (estados, tipos, materiais, ...)  ler: todos | escrever: admin
  Clientes, moradas, pacientes, pedidos, notas, ...  ler e escrever: admin e colaborador
  Encomendas        ler: todos (o cliente só vê as SUAS) | escrever: admin e colaborador
  Notificações      ler: todos (cada um só vê as suas; admin vê todas) | escrever: admin
                    PATCH /notificacoes/{id}/lida: o dono marca como lida

ESTRUTURA DA API
  api/app/main.py            arranque e registo das rotas
  api/app/db.py              ligação ao PostgreSQL (pool) e transações
  api/app/seguranca.py       passwords e tokens JWT
  api/app/dependencias.py    autenticação e permissões por tipo
  api/app/erros.py           erros da BD -> mensagens claras (409, 400, ...)
  api/app/servicos.py        registo e criação de utilizadores (várias tabelas, 1 transação)
  api/app/repositories/      SQL de cada tabela (substitui django/laboratorio/database/)
  api/app/routers/           endpoints

NOTAS
- Para acrescentar uma tabela nova: criar o ficheiro em api/app/repositories/
  (copiar um existente) e acrescentar uma linha em api/app/routers/tabelas.py.
- Não coloques a password real da BD em ficheiros partilhados nem no Git:
  usa só o api/.env. A password que estava no settings.py antigo ficou no
  histórico do Git; convém alterá-la no PostgreSQL.
