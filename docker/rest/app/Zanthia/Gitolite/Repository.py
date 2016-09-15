

class Repository():
    def __init__(self, init):
        if isinstance(init, dict):
            self.name = init['name']
            self.access = init['access']
        else:
            self.name = init.replace('repo ', '')
            self.name = self.name.replace('\n', '')
            self.access = {}

    def parse_user(self, init):
        splitted = init.split("=")
        map(str.strip, splitted)
        user_or_group = splitted[1].strip()
        access = splitted[0].strip()
        self.access[user_or_group] = access

    def __str__(self):
        users_string = '\n'.join(['    %s = %s' % (access, name) for (name, access) in self.access.items()])
        return 'repo %s\n%s\n' % (self.name, users_string)
