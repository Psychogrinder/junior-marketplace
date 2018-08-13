#!/bin/bash

cd marketplace.app

source .venv/bin/activate

export FLASK_APP=runserver.py
export FLASK_DEBUG=1

flask run --port=8000
