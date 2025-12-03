FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные библиотеки, нужные для psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
