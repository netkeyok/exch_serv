# Используем официальный базовый образ Oracle Linux 8
FROM oraclelinux:8

# Установка Oracle Instant Client
RUN dnf -y install oracle-release-el8 && \
dnf -y install oracle-instantclient19.21-basic oracle-instantclient19.21-devel && \
dnf -y install gcc python3-devel && \
dnf clean all

# Установка Python 3.11
RUN dnf -y module enable python311 && \
dnf -y install python311 && \
alternatives --set python /usr/bin/python3.11 && \
python3.11 -m ensurepip && \
python3.11 -m pip install --upgrade pip

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