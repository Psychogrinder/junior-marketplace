#!/bin/bash
set -e

source ../DOCKER_ENV_PRODUCTION
source ../.env.prod

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace && true
docker volume create marketplace_user_image
docker volume create marketplace_tasks
<<<<<<< HEAD

=======
docker volume create marketplace_chat

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace
>>>>>>> 45360da21ae4970ba390ce552541a20a3282f329

docker-compose -f docker-compose-prod.yml up --build $1
