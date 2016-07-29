FROM alpine:3.3

RUN apk add --no-cache sudo git docker py-pip perl openssh python && \
    pip install docker-compose && \
    rm -rf /var/cache/apk/*

RUN echo -e "Port 22\n" >> /etc/ssh/sshd_config && \
    echo -e "PubkeyAuthentication yes\n" >> /etc/ssh/sshd_config && \
    echo -e "RSAAuthentication yes\n" >> /etc/ssh/sshd_config && \
    echo -e "DOCKER_HOST='unix:///tmp/docker.sock'\n" >> /etc/conf.d/docker && \
    ssh-keygen -A && \
    mkdir -p /app && \
    mkdir -p /var/git && \
    mkdir -p /var/git/bin && \
    mkdir -p /var/git/local/hooks/common && \
    mkdir -p /var/git/zanthia && \
    mkdir -p /var/git/.ssh

# Prep users
RUN adduser -D -s /bin/sh -h /var/git gitolite && \
    adduser gitolite docker && \
    passwd -u gitolite && \
    echo -e "gitolite ALL=(root) NOPASSWD: /usr/bin/docker\ngitolite ALL=(root) NOPASSWD: /usr/bin/docker-compose\n" >> /etc/sudoers

RUN git clone git://github.com/sitaramc/gitolite /var/git/gitolite && \
    chown -R gitolite:gitolite /var/git && \
    su gitolite -c "/var/git/gitolite/install -to /var/git/bin"

COPY run.sh /var/git/run.sh

# Create docker socket
ENTRYPOINT ["/var/git/run.sh"]
