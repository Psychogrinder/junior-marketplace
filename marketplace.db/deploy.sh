#!/usr/bin/env bash

source ../DOCKER_ENV_STAGE

docker volume create marketplacedb
docker volume create marketplace.app

docker network create marketplace

docker-compose up --build
