#!/bin/bash

cd marketplace.app

source .venv/bin/activate

pip3 install -r requirements.txt

export FLASK_APP=runserver.py
export FLASK_DEBUG=1

flask run --port=8000
