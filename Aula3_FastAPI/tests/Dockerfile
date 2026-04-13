FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

#Copia o requirements que está na pasta tests
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copia a pasta app
COPY app ./app

#Copia a pasta tests para dentro do container
COPY tests ./tests

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]