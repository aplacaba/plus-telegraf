FROM telegraf:1.27-alpine

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pytz requests

COPY telegraf.conf /etc/telegraf/telegraf.conf
COPY scripts /tmp/scripts


EXPOSE 8125 8092 8094

RUN telegraf config /etc/telegraf/telegraf.conf
