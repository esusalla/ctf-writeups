FROM alpine

# expose required ports
EXPOSE 8001

# update repositories and install required packages
RUN apk update
RUN apk add alpine-sdk git linux-headers python3

# download and install radare2
RUN cd /root && git clone https://github.com/radareorg/radare2.git && cd radare2
RUN echo '#!/bin/sh' > /root/custom.sh 
RUN tail -n+11 /root/radare2/sys/install.sh >> /root/custom.sh
RUN cp /root/custom.sh /root/radare2/sys/custom.sh
RUN cd /root/radare2 && chmod +x ./sys/custom.sh && ./sys/custom.sh --with-capstone5

# set up application
RUN mkdir /app
COPY ./nx-oopsie /app
COPY ./server.py /app

# default command
CMD ["python3", "/app/server.py"]

