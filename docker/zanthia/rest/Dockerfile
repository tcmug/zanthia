FROM alpine:3.3

# Pre-install uwsgi:
RUN apk add --no-cache \
        python \
        uwsgi \
        py-pip \
        uwsgi-router_uwsgi \
        uwsgi-python \
        sudo \
        git \
        openssh \
        py-jinja2 \
        docker && \
    pip install paste flask flask_httpauth && \
    rm -rf /var/cache/apk/*

# Prep directories:
RUN mkdir -p /srv/rest-server/.ssh

# Prep users:
RUN adduser -D -s /bin/sh -h /srv/rest-server www && \
    passwd -u www && \
    echo -e "www ALL=(root) NOPASSWD: /usr/bin/docker\nwww ALL=(root) NOPASSWD: /usr/bin/docker-compose\n" >> /etc/sudoers

COPY run.sh /srv/run.sh
COPY uwsgi.ini /srv/rest-server/uwsgi.ini
ADD app /srv/rest-server/app
RUN chown www:www /srv/rest-server/.ssh

COPY run.sh /srv/run.sh
ADD app /srv/rest-server/app

RUN echo -e "Host git\n\tStrictHostKeyChecking no\n" >> /srv/rest-server/.ssh/config
RUN chown -R www:www /srv/rest-server/app
RUN su www -c "git config --global user.email 'zanthia@localhost'" && \
    su www -c "git config --global user.name 'Zanthia'" && \
    mkdir -p /etc/apache2/vhosts

ENV GIT_SSH_COMMAND: ssh -i /zanthia-shared/git_rsa

EXPOSE 8080

ENTRYPOINT ["/srv/run.sh"]
