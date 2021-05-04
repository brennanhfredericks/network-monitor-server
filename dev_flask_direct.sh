#!/bin/bash

docker-compose down

docker-compose -f "docker-compose-dev-flask-api.yml" build #--no-cache 

docker-compose -f "docker-compose-dev-flask-api.yml" up -d

docker ps

