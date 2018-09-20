#!/bin/bash

docker volume create marketplacedb
docker volume create marketplaceapp
docker volume create marketplaceimages

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 marketplace
