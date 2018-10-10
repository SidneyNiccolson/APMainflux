
Make sure that the docker-compose-dev.yml is configured to the mainflux docker network. Perform the following steps:

```sh
$ docker network ls
```
Copy the NETWORK ID for "docker_mainflux-base-net"
```sh
$ docker inspect <networkID__of_docker_mainflux-base-net>
```
Check if "apmainflux_user_1" is in the list of the network. 

Next verify in the same "docker inspect output" if the mainflux-nginx ip-address is the same 
as in the APmainflux docker-compose.yml denoted in the MAINFLUX_BROKER_URL environment variable.
