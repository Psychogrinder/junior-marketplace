#!/bin/bash

docker volume create marketplace.db
docker volume create marketplace.app

docker network create marketplace
