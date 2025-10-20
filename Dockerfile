# Base Python leve
FROM python:3.11-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho dentro do container
WORKDIR /app

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