FROM binexp-2.27

# expose required ports
EXPOSE 8000

# set up application
WORKDIR /app
COPY ./oversight ./

# default command
CMD ["socat", "TCP-LISTEN:8000,reuseaddr,fork", "EXEC:/app/oversight"]
