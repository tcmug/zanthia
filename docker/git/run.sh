#!/bin/sh

if [ ! -f /var/git/.ssh/id_rsa ]; then
    ssh-keygen -f /var/git/.ssh/id_rsa -N "" -t rsa
    chown -R gitolite:gitolite /var/git/.ssh
    su gitolite -c "/var/git/bin/gitolite setup -pk /var/git/.ssh/id_rsa.pub"
    sed -i '/%RC = .*/aLOCAL_CODE => \"$ENV{HOME}/local\",' /var/git/.gitolite.rc
    ln -s /app/src/post-receive /var/git/local/hooks/common/post-receive
    su gitolite -c "/var/git/bin/gitolite setup"
    cp /var/git/.ssh/id_rsa /app/git_rsa
fi

/usr/sbin/sshd -D -f /etc/ssh/sshd_config
