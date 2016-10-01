#!/bin/sh

# Generate a self signed key if it does not already exist.
if [ ! -f /etc/apache2/crt/server.key ]; then
    cd /etc/apache2/crt
    openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    openssl rsa -passin pass:x -in server.pass.key -out server.key
    rm server.pass.key
    openssl req -new -key server.key -out server.csr \
      -subj "/C=UK/ST=Warwickshire/L=Leamington/O=OrgName/OU=IT Department/CN=example.com"
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
fi

# Make sure no pid file exists.
if [ -f  /run/apache2/httpd.pid ]; then
    rm /run/apache2/httpd.pid
fi

# Copy config in place.
sed 's@{{ ZANTHIA_SERVERNAME }}@'"$ZANTHIA_SERVERNAME"'@' /etc/apache2/conf.d/vhost.conf.tmpl > /etc/apache2/conf.d/vhost.conf

exec /usr/sbin/httpd -f /etc/apache2/httpd.conf -D FOREGROUND
