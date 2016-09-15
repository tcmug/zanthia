
import re

class Group():
    def __init__(self, init):
        if isinstance(init, dict):
            self.name = init['name']
            self.users = init['users']
        else:
            splitted = init.split("=")
            map(str.strip, splitted)
            self.name = splitted[0].strip()
            self.users = re.findall(r'\S+', splitted[1])
            map(str.strip, self.users)

    def get_users(self):
        return self.users

    def __str__(self):
        return "%s = %s" % (self.name, " ".join(self.users))
