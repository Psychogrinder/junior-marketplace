#!/bin/bash

set -x
cd marketplace.app

source .venv/bin/activate

export FLASK_APP=runserver.py
export FLASK_DEBUG=1

#Перед запуском убедитесь, что у вас запущен postgres в доккере
#И создана marketplace.db на сервере.

if [ -d "migrations" ]; then
  rm -rf migrations
fi
flask db init
flask db migrate
flask db upgrade

flask run --port=8000
