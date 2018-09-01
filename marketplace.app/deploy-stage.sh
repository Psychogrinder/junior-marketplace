#!/bin/bash

if [[ $1 == 's' ]]
then
  source ../DOCKER_ENV_STAGE
else
  source ../.env.stage
fi

docker volume create marketplaceapp

docker network create marketplace

docker-compose -f docker-compose-stage.yml up --build
