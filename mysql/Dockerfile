FROM mysql:5.7.33

WORKDIR /init

COPY . /init

RUN chmod +x init.sh

# need to wait for mysql to start up
#CMD ["./init.sh"]