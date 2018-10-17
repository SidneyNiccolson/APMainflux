# AstroPlant-Mainflux 


This repository contains microservices to interface with Mainflux (https://mainflux.readthedocs.io/en/latest/). The main structure is a back-end Flask application
that communicates with Mainflux and a Reactjs front-end interfacing with the Flask API. Read more in [here](./mainflux_concept.md).


### Setup Mainflux
It is recommended to follow the read the docs or the following tutorial: https://medium.com/mainflux-iot-platform/mainflux-open-source-iot-platform-set-up-and-usage-70bed698791a

Prerequisites:
  - Git
  - Docker
  - Docker compose


```sh
$ git clone https://github.com/mainflux/mainflux.git
```
Start the influxDb writer & reader + the normal core services: 
```sh
docker-compose -f docker/docker-compose.yml -f docker/addons/influxdb-writer/docker-compose.yml -f docker/addons/influxdb-reader/docker-compose.yml up -d
```

### Getting started with AstroPlant-Mainflux client application

Prerequisites:
  - Git
  - Docker
  - Docker compose
  - npm
  - node
  
```sh
$ git clone https://github.com/SidneyNiccolson/APMainflux.git
```
Export React env. variable to point to flask service in the root folder of the project:
```sh
export REACT_APP_USERS_SERVICE_URL=http://localhost:81
```

Build the container and run the services:
```sh
docker-compose -f docker-compose-dev.yml up -d --build
```
Go to http://localhost:81/users/ping to check if API service is running

Go to http://localhost:81/ to see if React is running correctly.


### Testing and debugging

If any issues arise related to docker network connection read [here](./connect_mainflux_docker_network.md)

(optional) Run unit test:
```sh
docker-compose -f docker-compose-dev.yml run users python manage.py test
```
(optional run test):
```sh
docker-compose -f docker-compose-dev.yml run client npm test
```
### example mainflux script
In the device_client folder a simple example script is available to test certain features of mainflux.

