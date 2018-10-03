#!/usr/bin/env bash

set -xe

source ../DOCKER_ENV_PRODUCTION

docker exec marketplace.app python3 manage.py init_db
