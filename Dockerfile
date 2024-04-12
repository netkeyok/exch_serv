# Используем указанный базовый образ
FROM oraclelinux:8-slim

# Установка Oracle Instant Client
RUN yum -y install oracle-release-el8 && \
yum-config-manager --enable ol8_oracle_instantclient && \
yum -y install oracle-instantclient19.8-basic oracle-instantclient19.8-devel && \
yum -y install gcc python3-devel && \
yum clean all

# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/usr/lib/oracle/19.8/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin


# Копирование файлов проекта в контейнер
COPY . .

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Команды, выполняемые при запуске контейнера
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8083"]