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

if [ -d "migrations" ]; then
  rm -rf migrations
fi
python manage.py init_db

cd ..
bin/create_content.sh
# flask run --port=8000
