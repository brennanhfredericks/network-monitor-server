#!/bin/bash

docker-compose down

docker-compose -f "docker-compose.yml" build #--no-cache 

docker-compose -f "docker-compose.yml" up #-d

#docker ps

