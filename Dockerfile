FROM telegraf:1.27-alpine

COPY telegraf.conf /etc/telegraf/telegraf.conf

EXPOSE 8125 8092 8094

RUN telegraf config /etc/telegraf/telegraf.conf
