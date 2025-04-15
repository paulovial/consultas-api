# Imagem base oficial do Python
FROM python:3.12

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências de sistema
RUN apt-get update \
  && apt-get install -y build-essential libpq-dev curl \
  && apt-get clean

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Cria diretório da aplicação
WORKDIR /app

# Copia apenas arquivos de dependência primeiro (para cache eficiente)
COPY pyproject.toml poetry.lock* /app/

# Instala dependências com Poetry sem criar venv
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-root

# Copia o restante da aplicação
COPY . /app/

# Expõe a porta 8000
EXPOSE 8000

# Define o PYTHONPATH explicitamente para o diretório da aplicação
ENV PYTHONPATH=/app

# Comando padrão
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

