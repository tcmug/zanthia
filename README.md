
Zanthia
===================

... is a work in progress proof of concept of providing a git remote which
automatically manages docker containers per branch.

Short description:

 - A dockerfile which provides provides a git remote
 - The container controls host machines docker for provisioning
   configuration within git branches

Demo
-------------

At the projects root folder, run:
```
docker-compose up
```

After the container is up and running, add the ssh key to be used:
```
$ ssh-add git_rsa
```

Clone the testing repository:
```
$ git clone ssh://gitolite@localhost:2222/testing
```

Copy the skeleton project from the src folder and commit it to the repository
```
$ cp -rf src/skeleton/* testing/
$ cd testing
$ git add .
$ git commit -m "Initial commit"
$ git push origin master
```

If everything went well, you should now see Zanthia spool up the docker
containers with Manannan (manager) and Gwydion (docker-compose driver).

Once finished, opening up the browser on [http://localhost:8080](http://localhost:8080) should show a Drupal 8 installation page.

Install the site this database configuration:

	Database name: drupal
	Database username: dbuser
	Database password: dbpass
	Host: database

Once installation has finished, edit the port assignment docker-compose.yml
from port 8080:80 to 8081:80. Then create a branch, commit and push:
```
$ git checkout -b test
$ git add .
$ git commit -m "Changed to another port"
$ git push origin test
```

Zanthia will now clone the master branch containers based on specs in
manannan.yml. Once the process has finished, a clone of the previous
installation is available in [http://localhost:8081](http://localhost:8081)
