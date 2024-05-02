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

### Git Stuff

`git pull`

`git push`

`git status` - Show status of repo (current branch, file changes) - Good for double checking stuff!!!

`git add .` - Add all files to be ready to commit (Check using git status to ensure only suitable files will be added!!! Only code files should be added!!! eg .py, .svelte, .js .ect)

`git commit` - Create a new commit with the files that have been added (make sure to push after this!!)

`git checkout <branch-name>` - Switch to specific branch (easier create branch on gitlab first)

**Merging should be done on the gitlab site**
