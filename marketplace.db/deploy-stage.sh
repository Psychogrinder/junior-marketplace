#!/usr/bin/env bash
set +x

# source ../DOCKER_ENV_STAGE
source ../.env.stage

docker volume create marketplacedb

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace

docker-compose -f stage/docker-compose.yml up --build
