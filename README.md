
Zanthia is a work in progress proof of concept of providing a git remote which
automatically manages docker containers per branch.

Components:
	- Gitolite: git server
	- Ansible: provisioning environment to a server
		No dependencies Debian 8 (jessie) provisioning
	- Vagrant: local testing environment

To demo:

Spin up the local vagrant box
$ vagrant up

Copy the generated git private key from the vagrant box to your local, e.g.
$ vagrant ssh -c "sudo cp /var/git/.ssh/id_rsa /vagrant/git_rsa"

Add the ssh key to be used:
$ ssh-add git_rsa

Clone the testing repository:
$ git clone git@192.168.123.123:testing

Copy the skeleton project from the src folder and commit it to the repository
$ cp -rf src/skeleton/* testing/
$ cd testing
$ git add .
$ git commit -m "Initial commit"
$ git push

If everything went well, you should now see Zanthia spool up the docker
containers with Manannan (manager) and Gwydion (docker-compose driver).

Once finished, opening up the browser on:
	http://192.168.123.123:8080

Should show a Drupal 8 installation page.

Install the site this database configuration:

	Database name: drupal
	Database username: dbuser
	Database password: dbpass
	Host: database

Once installation has finished, edit the port assignment docker-compose.yml
from port 8080:80 to 8081:80. Then create a branch, commit and push:

$ git checkout -b test
$ git add .
$ git commit -m "Changed to another port"
$ git push

Zanthia will now clone the master branch containers based on specs in
manannan.yml. Once the process has finished, a clone of the previous
installation is available in:
	http://192.168.123.123:8081
