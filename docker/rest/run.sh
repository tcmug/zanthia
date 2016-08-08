#!/bin/sh

#sleep 10
cp -rf /app/git_rsa /var/zanthia/.ssh/id_rsa
chmod 400 /var/zanthia/.ssh/id_rsa

uwsgi --plugins-dir /usr/lib/uwsgi --ini /etc/uwsgi/apps-enabled/zanthia.ini
