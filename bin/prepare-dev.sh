#!/bin/bash

docker volume create marketplacedb
docker volume create marketplaceapp
docker volume create marketplaceimages

docker network create marketplace
