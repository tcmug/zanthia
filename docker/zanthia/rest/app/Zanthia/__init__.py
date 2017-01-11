
import sys
import os
import re
import subprocess

def shell_exec(params, capture = False):
    prev_dir = os.getcwd()
    sys.stdout.flush()
    # params.insert(0, "sudo")
    my_env = os.environ.copy()
    my_env["HOME"] = "/srv/rest-server/"
    my_env["user"] = "www"
    print my_env
    print " ".join(params)
    if capture:
        proc = subprocess.Popen(params, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=my_env)
        retval, err = proc.communicate()
        # print(retval)
        # print(err)
    else:
        retval = subprocess.call(params, env=my_env)
        os.chdir(prev_dir)
    return retval


from Gitolite import *


class Git():

    def __init__(self):

        if not os.path.isdir('gitolite-admin'):
            self._git([
                "clone",
                "gitolite@git:gitolite-admin"
            ])

        prev_dir = os.getcwd()
        os.chdir("gitolite-admin")
        shell_exec([
           "git",
           "pull"
        ])
        os.chdir(prev_dir)

        self.repos = {}
        self.groups = {}
        self.users = {}

        keydir = 'gitolite-admin/keydir';
        for path, subdirs, files in os.walk(keydir):
            for name in files:
                keyfile = os.path.join(path, name)
                self._parse_keyfile(keyfile)

        repo = False
        with open('gitolite-admin/conf/gitolite.conf', 'r') as file:
            for line in file.readlines():
                if line.startswith("repo"):
                    repo = Gitolite.Repository(init=line)
                    self.add_repo(repo)
                if line.startswith("@"):
                    group = Gitolite.Group(init=line)
                    self.add_group(group)
                elif "=" in line:
                    repo.parse_user(line)

    def _parse_keyfile(self, keyfile):
        head, tail = os.path.split(keyfile)
        name = os.path.splitext(tail)[0]
        if name in self.users:
            user = self.users[name]
        else:
            user = Gitolite.User(name)
            self.users[name] = user
        user.add_key_file(keyfile)

    def get_repositories(self):
        return self.repos.values()

    def get_groups(self):
        return self.groups.values()

    def get_users(self):
        return self.users.values()



    def add_group(self, group):
        self.groups[group.name] = group

    def delete_group(self, group_name):
        if group_name in self.groups:
            del self.groups[group_name]



    def add_repo(self, repo):
        self.repos[repo.name] = repo

    # def delete_repo(self, repo):
    #   TODO: this needs some trickery as gitolite does physically delete.

    def save(self):
        with open('/srv/rest-server/app/gitolite-admin/conf/gitolite.conf', 'w') as file:
            file.write(self.get_config())

        prev_dir = os.getcwd()
        os.chdir('/srv/rest-server/app/gitolite-admin')
        self._git(['status'])
        self._git(['add', '-A'])
        self._git(['commit', '-m "Changes via REST."'])
        self._git(['push', 'origin', 'master'])
        os.chdir(prev_dir)

    def get_config(self):
        return "\n".join(str(x) for x in self.get_groups()) + "\n\n" + "\n".join(str(x) for x in self.get_repositories())


    def _git(self, cmds):
        shell_exec([
            'git'
        ] + cmds)

