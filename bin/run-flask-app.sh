#!/bin/bash

cd marketplace.app

source .env/bin/activate

export FLASK_APP=runserver.py
export FLASK_DEBUG=1

flask run --port=8000