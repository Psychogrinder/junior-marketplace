#!/bin/bash
set -x

docker container stop marketplace.db
docker container rm marketplace.db
docker volume rm marketplacedb
docker volume create marketplacedb
cd marketplace.db
docker-compose up -d --build && cd ../marketplace.app

source .venv/bin/activate

pip3 install -r requirements.txt
export FLASK_APP=runserver.py
export FLASK_DEBUG=1

<<<<<<< HEAD
=======
#Перед запуском убедитесь, что у вас запущен postgres в доккере
#И создана marketplace.db на сервере.

>>>>>>> 6410d36055ab9294d8a67f9f4db48fb5c8ca1295
if [ -d "migrations" ]; then
  rm -rf migrations
fi
flask db init
flask db migrate
flask db upgrade

cd ..
bin/create_content.sh
# flask run --port=8000
