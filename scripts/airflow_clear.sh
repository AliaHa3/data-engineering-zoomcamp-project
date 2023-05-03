source scripts/setup_config.sh
cd airflow
## To stop and delete containers, delete volumes with database data, and download images, run:
docker-compose down --volumes --rmi all
docker-compose down --volumes --remove-orphans
