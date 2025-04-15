# Consultas API

API RESTful para gerenciamento de consultas médicas. Desenvolvida com Django, Django REST Framework, PostgreSQL, Docker e Poetry. Possui integração com sistema de pagamento (Asaas - mock) e deploy em ambiente de produção via AWS EC2.

## Stack Tecnológica

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- Poetry (gerenciador de dependências)
- GitHub Actions (CI)
- AWS EC2 (Staging/Produção)

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
poetry install
```

4. Configure o banco de dados PostgreSQL local e o `.env` (caso necessário).

5. Rode as migrações:

```bash
python manage.py migrate
```

6. Execute o servidor:

```bash
python manage.py runserver
```

## Setup com Docker

1. Construa e inicie os containers:

```bash
docker-compose up --build
```

2. O backend estará acessível em `http://localhost:8000`.

## Execução do Projeto

- Endpoint de healthcheck: `GET /api/health/`
- Cadastro e listagem de profissionais: `GET/POST /api/profissionais/`
- Registro de consultas: `GET/POST /api/consultas/`
- Mock de pagamento: `POST /api/pagamentos/mock/`

## Testes Automatizados

Os testes utilizam `APITestCase` do Django REST Framework. Para executá-los:

```bash
python manage.py test
```

Ou, caso esteja usando o Poetry:

```bash
poetry run python manage.py test
```

