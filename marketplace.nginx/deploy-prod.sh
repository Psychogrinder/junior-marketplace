#!/bin/bash

source ../DOCKER_ENV_PRODUCTION

docker-compose -f production/docker-compose.yml up -d --build
