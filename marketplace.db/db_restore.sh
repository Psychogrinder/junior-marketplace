#!/usr/bin/env bash

set -x

source ../DOCKER_ENV_PRODUCTION

if [[ $2 == "create" ]]
then
  docker exec marketplace.db psql -c 'create database "marketplace.db";' -U postgres
fi

zcat $1 | docker exec -i marketplace.db psql -U postgres -d marketplace.db
