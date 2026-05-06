FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install fastapi uvicorn psycopg2-binary prometheus-client pyjwt prometheus-fastapi-instrumentator sqlalchemy alembic 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
