#!/bin/bash

pwd
sudo chmod -R 777 dbt
cd airflow
docker-compose build
docker-compose up airflow-init
docker-compose up -d
echo "Run 'docker-compose logs --follow' to see the logs."