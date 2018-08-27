#!/bin/bash

source ../DOCKER_ENV_STAGE

docker-compose -f docker-compose-stage.yml up --build
