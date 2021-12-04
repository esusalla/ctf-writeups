from ubuntu:18.04

EXPOSE 8080

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install -y build-essential curl libpcre3-dev libssl-dev nginx tcl-dev vim wget

RUN wget https://archive.apache.org/dist/trafficserver/trafficserver-7.1.1.tar.bz2
RUN tar -xf trafficserver-7.1.1.tar.bz2
RUN cd trafficserver-7.1.1 && \
    ./configure --prefix=/opt/ats && \
    make && \
    make install

COPY ./remap.config /opt/ats/etc/trafficserver/
COPY ./public/* /var/www/html/

RUN /opt/ats/bin/trafficserver start
RUN service nginx restart
