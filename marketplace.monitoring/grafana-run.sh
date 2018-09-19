#!/usr/bin/env bash
set +x

docker run -d --name=grafana -v grafana_vol:/var/lib/grafana/ -p 3000:3000 grafana/grafana
