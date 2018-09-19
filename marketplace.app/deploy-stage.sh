#!/bin/bash

if [[ $1 == 's' ]]
then
  source ../DOCKER_ENV_STAGE
else
  source ../.env.stage
fi

docker volume create marketplaceapp

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace

docker-compose -f docker-compose-stage.yml up --build
