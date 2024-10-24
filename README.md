# DESD

## Install instructions

Navigate to the root directory of the repository and run:

`cd smartcare-svelte`

`npm install`

`docker-compose up --build` 

You can add the flag `-d` to daemonise the processes

Currently there are three containers:

1. web-rest
2. web-svelte
3. db

To execute terminal commands to any of these containers use the command `docker-compose exec <container name> <command>`

For example, to run django migrations you would use the command `docker-compose exec web-rest python manage.py migrate`
