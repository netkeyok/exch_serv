# Используем официальный базовый образ Oracle Linux 8
FROM ghcr.io/oracle/oraclelinux:8

ARG release=19
ARG update=21

# Установка Python и необходимых пакетов
RUN dnf -y install \
    python3.11 python3.11-pip python3.11-setuptools python3.11-wheel \
    epel-release && \
    rm -rf /var/cache/dnf

# Установка переменных окружения для Oracle Instant Client
ENV ORACLE_HOME=/usr/lib/oracle/${release}.${update}/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV FLOWER_TIMEZONE=Asia/Yekaterinburg
ENV PYTHONUNBUFFERED=1

# Копирование и установка Oracle Instant Client из локальных RPM-файлов
COPY OraCliInstall/oracle-instantclient${release}.${update}-basic-*.rpm /tmp/
COPY OraCliInstall/oracle-instantclient${release}.${update}-devel-*.rpm /tmp/
COPY OraCliInstall/oracle-instantclient${release}.${update}-sqlplus-*.rpm /tmp/
RUN dnf -y localinstall /tmp/oracle-instantclient${release}.${update}-basic-*.rpm /tmp/oracle-instantclient${release}.${update}-devel-*.rpm /tmp/oracle-instantclient${release}.${update}-sqlplus-*.rpm && \
    rm -f /tmp/*.rpm

# Установка supervisord через pip
RUN pip3 install supervisor

# Копирование файлов проекта в контейнер
COPY . .

# Обновление pip и установка зависимостей
RUN python3.11 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

# Настройка Python 3.11 как версии по умолчанию для python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Настройка прав на файл supervisord.conf
RUN chmod 644 /supervisord.conf

# Команды, выполняемые при запуске контейнера
CMD ["supervisord", "-c", "supervisord.conf"]
