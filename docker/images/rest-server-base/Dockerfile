FROM alpine:3.3

# Pre-install uwsgi:
RUN apk add --no-cache \
        python \
        uwsgi \
        py-pip \
        uwsgi-router_uwsgi \
        uwsgi-python && \
    pip install paste flask flask_httpauth && \
    rm -rf /var/cache/apk/*

# Prep directories:
RUN mkdir -p /srv/rest-server

# Prep users:
RUN adduser -D -s /bin/sh -h /srv/rest-server www && \
    passwd -u www

COPY run.sh /srv/run.sh
COPY uwsgi.ini /srv/rest-server/uwsgi.ini
ADD app /srv/rest-server/app

EXPOSE 8080

ENTRYPOINT ["/srv/run.sh"]
