#!/bin/bash
set -e

source ../DOCKER_ENV_PRODUCTION
source ../.env.prod

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace && true
docker volume create marketplace_user_image
docker volume create marketplace_tasks


docker-compose -f docker-compose-prod.yml up --build $1
