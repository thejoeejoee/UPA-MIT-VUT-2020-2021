# UPA MIT-VUT@2020-2021

## Requirements
* Docker engine
* Docker compose

## Launch
``
1. Initialize docker
docker-compose up

2. Create user for superset:
docker-compose exec superset superset-init

3. Login to superset and add connect postgres:
Sources -> Databases -> +
SQLAlchemyURI: postgresql://superset:superset@postgres/upa    

4. 
docker-compose run --rm django-admin migrate
docker-compose up computer
``