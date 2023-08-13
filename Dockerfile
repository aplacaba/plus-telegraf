FROM telegraf:1.27-alpine

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

COPY telegraf.conf /etc/telegraf/telegraf.conf
COPY data_import.py /tmp/data_import.py


EXPOSE 8125 8092 8094

RUN telegraf config /etc/telegraf/telegraf.conf
