# Frontend Dockerfile
FROM python:3.9-slim-bullseye

WORKDIR /app

# Instala dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API
COPY frontend/ .

# Expõe a porta do Flask
EXPOSE 52035

# Executa o Flask na inicialização
CMD ["flask", "run", "--host=0.0.0.0", "--port=52035"]
