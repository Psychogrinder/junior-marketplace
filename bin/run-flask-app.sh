#!/bin/bash

cd marketplace.app

source .venv/bin/activate
source ../.env.local
pip3 install -r requirements.txt


flask run --port=8000
