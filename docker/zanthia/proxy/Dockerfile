
FROM alpine:3.3

RUN apk add --no-cache \
        apache2 \
        apache2-proxy \
        apache2-ssl \
        openssl \
        python \
        py-jinja2 \
        docker \
        supervisor \
        inotify-tools \
        sudo && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /run/apache2 && \
    mkdir -p /etc/apache2/vhosts && \
    mkdir -p /etc/apache2/crt

ADD apache/conf.d/proxy.conf /etc/apache2/conf.d/proxy.conf
ADD apache/conf.d/vhost.conf /etc/apache2/conf.d/vhost.conf
ADD watcher.sh /srv/watcher.sh
ADD apache.sh /srv/apache.sh

COPY supervisord.conf /etc/supervisord.conf

VOLUME /etc/apache2/vhosts

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
