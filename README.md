# UPA FIT-VUT@2020-2021

Dockerized application for fetching, parsing, processing, annotating and displaying meteorological from Australia.

## Requirements
* Docker engine
* Docker compose

## Filling Environment Variables
Create file ```.local.env``` and fill it according to ```.local.env.template```.

```SUPSERSET_SECRET```, ```SECRET_KEY``` - has to be random and static for each instance of project

```MAPBOX_API_KEY``` - API access token for [Mapbox](https://www.mapbox.com) needed for viewing maps in Superset

```LOG_LEVEL``` - logging level corresponding to python logging levels

## Initialization of services
1. Initialize and run docker containers:
    * Run contaners (but next steps must be done in another CLI):
        * ```make up```
    * Run detached containers:
        * ```make upd```
1. Wait until all containers are running and then initialize superset and create admin user:
    * ```make init```
1. Initialize database and dashboards:
    * ```make restore-superset```

## Stopping services
To stop all services just run:
* ```make down```

## Managing data
To append data to NoSQL database create directory ```pocasi``` and copy dataset there. Then run command: 
* ```make scrape```

To update SQL database with data computed from NoSQL database run:
* ```make compute```

## Managing users
Creating users and admins can be done in two ways. It can be done through Superset GUI (provided that there is at least one admin account created) or CLI.

To add admin through CLI:
* ```make create-admin```

To add user through CLI:
* ```make create-user```

## Help
To show help run:
* ```make help```


## Service ports
Service | Port
------- | ----
[mongo-admin](http://localhost:8081) | 8081
[postgres-admin](http://localhost:8082) | 8082
[superset](http://localhost:8088) | 8088
postgres | 5432
mongo | 27017
redis | 6379
