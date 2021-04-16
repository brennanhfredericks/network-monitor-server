FROM mysql:5.7.33

WORKDIR /init

COPY . /init


RUN apt-get update -y
RUN apt-get install nano -y
RUN chmod +x init.sh

#CMD ["./init.sh"]