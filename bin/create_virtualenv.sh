#!/bin/bash

virtualenv -p python3 ./marketplace.app/.env
source ./marketplace.app/.env

pip3 install -r ./marketplace.app/requirements.txt
