FROM alpine:3.3

RUN apk add --no-cache sudo git python uwsgi py-pip uwsgi-router_uwsgi uwsgi-python openssh && \
    pip install paste flask flask-assets jsmin && \
    rm -rf /var/cache/apk/*

RUN mkdir /var/zanthia && \
    mkdir /app && \
    mkdir /var/zanthia/app && \
    mkdir -p /var/zanthia/.ssh

# Prep users
RUN adduser -D -s /bin/sh -h /var/zanthia www && \
    passwd -u www && \
    chown www:www /var/zanthia/.ssh

COPY run.sh /var/zanthia
COPY zanthia.ini /etc/uwsgi/apps-enabled/
ADD app /var/zanthia/app

RUN echo -e "Host git\n\tStrictHostKeyChecking no\n" >> /var/zanthia/.ssh/config

RUN chown www:www /var/zanthia

# Create docker socket
ENTRYPOINT ["/var/zanthia/run.sh"]
