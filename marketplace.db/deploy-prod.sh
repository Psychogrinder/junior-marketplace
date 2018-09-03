#!/usr/bin/env bash

source ../DOCKER_ENV_PRODUCTION

docker volume create marketplacedb

docker network create marketplace

docker-compose -f prod/docker-compose.yml up --build
