# Base Python leve
FROM python:3.11-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho dentro do container
WORKDIR /app

# Declara os argumentos que virão do build
ARG ACCESS_TOKEN
ARG ACCESS_TOKEN_SECRET
ARG CONSUMER_KEY
ARG CONSUMER_SECRET
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION
ARG BUCKET_NAME

# Define as variáveis de ambiente no contêiner
ENV ACCESS_TOKEN=$ACCESS_TOKEN \
    ACCESS_TOKEN_SECRET=$ACCESS_TOKEN_SECRET \
    CONSUMER_KEY=$CONSUMER_KEY \
    CONSUMER_SECRET=$CONSUMER_SECRET \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    AWS_REGION=$AWS_REGION \
    BUCKET_NAME=$BUCKET_NAME

# Copia apenas requirements primeiro para usar cache
COPY requirements.txt .

# Instala dependências de sistema e Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o projeto
COPY . .

# Define o entrypoint para python3, para que comandos do AWS Batch possam ser passados dinamicamente
ENTRYPOINT ["python3"]

# Define um CMD default, que pode ser sobrescrito pelo Batch
CMD ["-m", "twitter_bot.main"]