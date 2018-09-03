#!/bin/bash

source ../DOCKER_ENV_STAGE

docker-compose -f stage/docker-compose.yml up -d --build
