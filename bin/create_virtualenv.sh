#!/bin/bash

virtualenv -p python3 ./marketplace.app/.venv
source ./marketplace.app/.venv

pip3 install -r ./marketplace.app/requirements.txt
