#!/usr/bin/env bash

set -e

source ../DOCKER_ENV_PRODUCTION

USER_IMAGE=$(docker inspect marketplace_user_image --format='{{.Mountpoint}}')

source ../.env.prod

mkdir -p $USER_IMAGE_DIR_NAME

scp -P $XTRAMARKET_SSH_PORT -r root@46.21.248.236:$USER_IMAGE $USER_IMAGE_DIR_NAME/

tar zcf $USER_IMAGE_DIR_NAME.tar.gz $USER_IMAGE_DIR_NAME/

source ../marketplace.app/.venv/bin/activate

python ya_dump.py && rm $USER_IMAGE_DIR_NAME.tar.gz && rm -r $USER_IMAGE_DIR_NAME
