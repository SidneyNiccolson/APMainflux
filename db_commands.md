## DB commands
Check database
  
```sh
$ docker exec -ti users-db psql -U postgres -W
```

Recreate database
```sh
$ docker-compose -f docker-compose-dev.yml run users python manage.py recreatedb
```
Migrate
```sh
 $ docker-compose -f docker-compose-dev.yml run users python manage.py db init
 $ docker-compose -f docker-compose-dev.yml run users python manage.py db migrate
 $ docker-compose -f docker-compose-dev.yml run users python manage.py db upgrade
 ```
 
 Checkout postgres database
 ```sh
 docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
  ```
