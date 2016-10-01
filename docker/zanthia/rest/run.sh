#!/bin/sh

while [ ! -f  /zanthia-shared/git_rsa ]
do
    echo "Waiting for ssh key to be generated..."
    sleep 2
done

chmod o+w /etc/apache2/vhosts

cp -rf /zanthia-shared/git_rsa /srv/rest-server/.ssh/id_rsa
chown -R gitolite:gitolite /srv/rest-server/.ssh
chmod 400 /srv/rest-server/.ssh/id_rsa

uwsgi --plugins-dir /usr/lib/uwsgi --ini /srv/rest-server/uwsgi.ini

