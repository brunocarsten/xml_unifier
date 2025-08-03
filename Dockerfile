FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY xml_unifier.py .
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Cria a pasta files para os XMLs de entrada
RUN mkdir -p files

# Define o comando padrão
CMD ["python", "xml_unifier.py"]
