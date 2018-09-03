#!/bin/bash
set -x

docker container stop marketplace.db
docker container rm marketplace.db
docker volume rm marketplacedb
docker volume create marketplacedb
if [[ $1 == 's' ]]
then
  source ../DOCKER_ENV_STAGE
  source ./.env.stage
else
  source ./.env.local
fi
cd marketplace.db
docker-compose up -d --build && cd ../marketplace.app

source .venv/bin/activate

pip3 install -r requirements.txt
export FLASK_APP=runserver.py
export FLASK_ENV=development

if [ -d "migrations" ]; then
  rm -rf migrations
fi
python3 manage.py init_db

cd ..
bin/create_content.sh
# flask run --port=8000
