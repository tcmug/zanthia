
FROM zanthia/rest-server-base

RUN apk add --no-cache sudo git openssh py-jinja2 docker && \
    rm -rf /var/cache/apk/*

RUN mkdir -p /srv/rest-server/.ssh

# Prep users
RUN chown www:www /srv/rest-server/.ssh

COPY run.sh /srv/run.sh
ADD app /srv/rest-server/app

RUN echo -e "Host git\n\tStrictHostKeyChecking no\n" >> /srv/rest-server/.ssh/config
RUN chown www:www /srv/rest-server/app
RUN su www -c "git config --global user.email 'zanthia@localhost'" && \
    su www -c "git config --global user.name 'Zanthia'" && \
    mkdir -p /etc/apache2/vhosts

ENV GIT_SSH_COMMAND: ssh -i /zanthia-shared/git_rsa
