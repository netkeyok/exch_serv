# Используем официальный базовый образ Oracle Linux 8
#FROM ghcr.io/oracle/oraclelinux8-python:3.11-amd64
FROM ghcr.io/oracle/oraclelinux:8


ARG release=19
ARG update=21

RUN dnf -y install python3.11 python3.11-pip python3.11-setuptools python3.11-wheel && \
     dnf -y install oracle-release-el8 && \
     dnf -y install oracle-instantclient${release}.${update}-basic oracle-instantclient${release}.${update}-devel oracle-instantclient${release}.${update}-sqlplus && \
     dnf -y install epel-release && \
     dnf -y install supervisor && \
     rm -rf /var/cache/dnf

# Установка переменных окружения для Oracle Instant Client

ENV ORACLE_HOME=/usr/lib/oracle/19.21/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV FLOWER_TIMEZONE=Asia/Yekaterinburg


# Копирование файлов проекта в контейнер
COPY . .

# RUN python3 -m pip install --upgrade pip \
#     && pip3 install --user -r requirements.txt

RUN chmod 644 /supervisord.conf

# Команды, выполняемые при запуске контейнера
#CMD ["supervisord", "-c", "supervisord.conf"]
CMD ["/bin/python3", "-V"]