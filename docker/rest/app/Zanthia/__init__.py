
import sys
import os
import re
import subprocess

def shell_exec(params, capture = False):
    prev_dir = os.getcwd()
    sys.stdout.flush()
    # params.insert(0, "sudo")
    print " ".join(params)
    if capture:
        proc = subprocess.Popen(params, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        retval, err = proc.communicate()
        # print(retval)
        # print(err)
    else:
        retval = subprocess.call(params)
        os.chdir(prev_dir)
    return retval


class GitoliteUser():
    def __init__(self, init):
        splitted = init.split("=")
        map(str.strip, splitted)
        self.name = splitted[1]
        self.access = splitted[0]

    def __str__(self):
        return "    %s %s" % (self.access, self.name)



class GitoliteGroup():
    def __init__(self, init):
        splitted = init.split("=")
        map(str.strip, splitted)
        self.name = splitted[0]
        self.users = re.findall(r'\S+', splitted[1])
        map(str.strip, self.users)

    def get_users(self):
        return self.users

    def __str__(self):
        return "%s = %s" % (self.name, " ".join(self.users))



class GitoliteRepository():
    def __init__(self, init):
        self.name = init.replace('repo ', '')
        self.name = self.name.replace('\n', '')
        self.users = []

    def parse_user(self, init):
        user = GitoliteUser(init)
        self.users.append(user)
        return user

    def __str__(self):
        users_string = '\n'.join(str(x) for x in self.users)
        return self.name + users_string



class Gitolite():

    def __init__(self):
        if not os.path.isdir('gitolite-admin'):
            shell_exec([
                "git",
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

        self.repos = []
        self.groups = []
        self.users = []
        repo = False
        with open('gitolite-admin/conf/gitolite.conf', 'r') as file:
            for line in file.readlines():
                if line.startswith("repo"):
                    repo = GitoliteRepository(init=line)
                    self.repos.append(repo)
                if line.startswith("@"):
                    group = GitoliteGroup(init=line)
                    self.groups.append(group)
                elif "=" in line:
                    user = repo.parse_user(init=line)
                    self.users.append(user)

    def get_repositories(self):
        return self.repos

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_config(self):
        return "\n".join(str(x) for x in self.groups) + "\n###\n" + "\n".join(str(x) for x in self.repos)



