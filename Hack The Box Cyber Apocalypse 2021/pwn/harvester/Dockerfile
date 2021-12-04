FROM ubuntu:18.04

# expose required ports
EXPOSE 8001

# update repositories and install required packages
RUN apt update -y
RUN apt install -y build-essential git python3

# download and install radare2
RUN cd /root && git clone https://github.com/radareorg/radare2.git && cd radare2
RUN echo '#!/bin/sh' > /root/custom.sh 
RUN tail -n+11 /root/radare2/sys/install.sh >> /root/custom.sh
RUN cp /root/custom.sh /root/radare2/sys/custom.sh
RUN cd /root/radare2 && chmod +x ./sys/custom.sh && ./sys/custom.sh --with-capstone5

# set up application
RUN mkdir /app
COPY ./harvester /app
COPY ./server.py /app

# default command
CMD ["python3", "/app/server.py"]

