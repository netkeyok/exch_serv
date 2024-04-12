# Используем указанный базовый образ
FROM ghcr.io/oracle/oraclelinux8-python:3.11-20240406-amd64


# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/usr/lib/oracle/19.8/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin


# Копирование файлов проекта в контейнер
COPY . .

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8083"]