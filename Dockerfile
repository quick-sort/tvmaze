FROM python:3.11
RUN apt-get update && \
    apt-get -y install cron && \
    mkdir -p /etc/cron.d && \
    mkdir -p /app/db

WORKDIR /app
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY app /app/app
COPY scripts /app/scripts
VOLUME /app/db
RUN mv /app/scripts/crontab /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab 
CMD cron && bash -x /app/scripts/start-server.sh 
