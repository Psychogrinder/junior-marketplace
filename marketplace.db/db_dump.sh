#!/usr/bin/env bash

set -x

source ../DOCKER_ENV_PRODUCTION

DUMP_DIR=$(docker inspect marketplacedb --format='{{.Mountpoint}}')

docker exec marketplace.db \
    pg_dump -U postgres marketplace.db | \
    gzip > marketplace_db._$(date "+%Y-%m-%d").sql.gz
