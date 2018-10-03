#!/usr/bin/env bash
set +e

source ../DOCKER_ENV_PRODUCTION
source ../.env.prod

docker volume create marketplace_monitor

docker-compose up --build $1
