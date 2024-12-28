# ML Dockerfile
FROM python:3.9-slim-bullseye

WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV DATASET_URL="https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds1.csv"

# Copia o código fonte
COPY ml-container/ .

# Configura o ponto de entrada
CMD ["python", "generate_rules.py"]
