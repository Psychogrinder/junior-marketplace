#!/usr/bin/env bash

set -e

source ../DOCKER_ENV_PRODUCTION

if [[ $2 == "create" ]]
then
  docker exec marketplace.db psql -c 'drop database "marketplace.db";' -U postgres
  docker exec marketplace.db psql -c 'create database "marketplace.db";' -U postgres
fi

zcat $1 | docker exec -i marketplace.db psql -U postgres -d marketplace.db
