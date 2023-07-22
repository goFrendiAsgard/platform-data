#!/bin/bash

docker compose down
docker volume prune

sudo rm -Rf airbyte/data
sudo rm -Rf airbyte/db
sudo rm -Rf airbyte/temporal
sudo rm -Rf airbyte/workspace

sudo rm -Rf airflow/config
sudo rm -Rf airflow/logs
sudo rm -Rf airflow/plugins
sudo rm -Rf airflow/postgres-data

sudo rm -Rf clickhouse
sudo rm -Rf metabase
sudo rm -Rf postgres-data