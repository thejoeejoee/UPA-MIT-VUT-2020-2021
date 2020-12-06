# UPA MIT-VUT@2020-2021

## Requirements
* Docker engine
* Docker compose

## Initialization of services
1. Initialize and run docker containers:
    * ```make run```
1. Wait until all containers are running and then initialize and create admin user for superset:
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
