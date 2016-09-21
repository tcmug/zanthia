#!/bin/sh

while inotifywait -e close_write /etc/apache2/vhosts; do
    supervisorctl restart apache
done

