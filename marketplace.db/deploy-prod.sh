#!/usr/bin/env bash

source ../DOCKER_ENV_PRODUCTION

docker volume create marketplacedb

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace

docker-compose -f prod/docker-compose.yml up --build -d
