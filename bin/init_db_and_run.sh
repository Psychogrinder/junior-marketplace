#!/bin/bash

cd marketplace.app

source .venv/bin/activate

export FLASK_APP=runserver.py
export FLASK_DEBUG=1

#Перед запуском убедитесь, что у вас запущен postgres в доккере
#И создана marketplace.db на сервере.

rm -rf migrations
flask db init
flask db migrate
flask db upgrade

flask run --port=8000
