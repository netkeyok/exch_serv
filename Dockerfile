# Используем официальный базовый образ Oracle Linux 8
FROM ghcr.io/oracle/oraclelinux:8

ARG release=19
ARG update=21

# Установка необходимых пакетов
RUN dnf -y install \
    python3.11 python3.11-pip python3.11-setuptools python3.11-wheel \
    epel-release && \
    rm -rf /var/cache/dnf

# Установка Oracle Instant Client из локальной папки
COPY OraCliInstall/oracle-instantclient${release}.${update}-*.rpm /tmp/
RUN dnf -y localinstall /tmp/oracle-instantclient${release}.${update}-*.rpm && \
    rm -rf /var/cache/dnf /tmp/oracle-instantclient${release}.${update}-*.rpm

# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/usr/lib/oracle/19.21/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV FLOWER_TIMEZONE=Asia/Yekaterinburg
ENV PYTHONUNBUFFERED=1

# Копирование файлов проекта в контейнер
COPY . /app
WORKDIR /app

# Обновление pip и установка зависимостей
RUN python3.11 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

# Установка Supervisor
RUN dnf -y install supervisor

# Копирование конфигурации Supervisor
COPY supervisord.conf /etc/supervisord.conf

# Разрешения на файл конфигурации Supervisor
RUN chmod 644 /etc/supervisord.conf

# Команды для запуска контейнера
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
