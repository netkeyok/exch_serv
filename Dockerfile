FROM ghcr.io/oracle/oraclelinux8-python:3.11-amd64


ENV PYTHONUNBUFFERED=1

RUN apk update


# Установка SQLAlchemy и pyodbc, копирование файлов проекта и установка зависимостей
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]