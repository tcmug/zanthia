
FROM alpine:3.3

RUN apk add --no-cache \
        apache2 \
        apache2-proxy \
        apache2-ssl \
        openssl \
        python \
        py-jinja2 \
        docker \
        sudo && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /run/apache2 && \
    mkdir -p /etc/apache2/vhosts && \
    mkdir -p /etc/apache2/crt

ADD apache/conf.d/proxy.conf /etc/apache2/conf.d/proxy.conf
ADD apache/conf.d/vhost.conf /etc/apache2/conf.d/vhost.conf
ADD run.sh /srv/run.sh

VOLUME /etc/apache2/vhosts

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["/srv/run.sh"]
