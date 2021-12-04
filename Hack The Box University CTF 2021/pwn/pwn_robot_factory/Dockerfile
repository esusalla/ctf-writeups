FROM ubuntu:20.04

RUN apt-get update && apt-get install -y build-essential git python3 socat vim

WORKDIR /app
COPY ./flag.txt /app
COPY ./robot_factory /app

# download and install radare2
RUN cd /root && git clone https://github.com/radareorg/radare2.git && cd radare2
RUN echo '#!/bin/sh' > /root/custom.sh 
RUN tail -n+11 /root/radare2/sys/install.sh >> /root/custom.sh
RUN cp /root/custom.sh /root/radare2/sys/custom.sh
RUN cd /root/radare2 && chmod +x ./sys/custom.sh && ./sys/custom.sh

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./robot_factory"] 
