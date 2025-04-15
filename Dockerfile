#Imagem base oficial do Python
FROM python:3.12

#Variaveis de ambiente para evitar criacao de arquivos .pyc e forcar UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias do sistema (build-essential, libpq para PostgreSQL, etc.)
RUN apt-get update \
  && apt-get install -y build-essential libpq-dev curl \
  && apt-get clean

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

#Cria diretorio da aplicacao
WORKDIR /app

#Copia apenas arquivos necessarios para instalar dependencias
COPY pyproject.toml poetry.lock* /app/

# Instala dependencias com Poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-root

# Copia o restante do codigo da aplicacao
COPY . /app/

# Expoe a porta 
EXPOSE 8000

# Comando padrao: inicia o servidor
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
