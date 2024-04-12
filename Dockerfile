# Используем официальный базовый образ Oracle Linux 8
FROM ghcr.io/oracle/oraclelinux8-python:3.11-amd64

# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/usr/lib/oracle/19.21/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin


# Копирование файлов проекта в контейнер
COPY . .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8083"]