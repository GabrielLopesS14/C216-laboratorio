# Definindo a imagem base
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /AULA2_REVISÃO_PYTHON_CRUD

# Copia um arquivo para o diretório de trabalho no container
COPY CRUD-alunos.py .

# Copia todos os arquivos do diretório app para o diretório de trabalho no container
# COPY ./AULA2_REVISÃO_PYTHON_CRUD .

# Define o comando de execução ao iniciar o container
CMD ["python" , "CRUD-alunos.py"]