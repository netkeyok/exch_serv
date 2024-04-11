 Используем официальный образ Python как базовый
FROM python:3.11

# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle/instantclient_19_8
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin

# Установка необходимых пакетов и зависимостей для Oracle Instant Client
RUN apt-get update && apt-get install -y libaio1 wget unzip \
&& mkdir -p /opt/oracle \
&& cd /opt/oracle

# Скачивание и установка Oracle Instant Client
# Обратите внимание, что ссылки на скачивание должны быть актуальными и доступными
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basiclite-linux.x64-19.8.0.0.0dbru.zip \
&& unzip instantclient-basiclite-linux.x64-19.8.0.0.0dbru.zip -d /opt/oracle \
&& rm -f instantclient-basiclite-linux.x64-19.8.0.0.0dbru.zip \
&& ln -s $ORACLE_HOME/libclntsh.so.19.1 $ORACLE_HOME/libclntsh.so \
&& ln -s $ORACLE_HOME/libocci.so.19.1 $ORACLE_HOME/libocci.so


# Копирование файлов проекта и установка зависимостей Python
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Инициализация OracleDB Thick Mode в Python скрипте
# Добавьте следующий код в начало вашего Python скрипта:
# import oracledb
# oracledb.init_oracle_client(lib_dir='/opt/oracle/instantclient_19_8', thick_mode=True)

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8083"]