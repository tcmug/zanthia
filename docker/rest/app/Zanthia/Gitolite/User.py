
import os

class User():

    def __init__(self, name):
        self.name = name
        self.keys = {}
        self.pubkey = ''
        self._changed_key_tags = []
        self._deleted_key_tags = []
        self._keys_base_dir = "gitolite-admin/keydir/"

    def save(self):
        for tag in self._changed_key_tags:
            dir = self._get_path_for_tag(tag)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file_name = dir + '/' + self.name + '.pub';
            with open(file_name, 'w') as f:
                f.write(self.keys[tag])

        for tag in self._deleted_key_tags:
            file = self._get_path_for_tag(tag) + '/' + self.name + '.pub';
            if os.path.isfile(file):
                os.remove(file)

    def add_key_file(self, keyfile):
        with open(keyfile, 'r') as f:
            key = f.read()
            tag = os.path.dirname(keyfile)
            tag = tag.split(os.sep)[-1]
            if tag == "keydir":
                tag = "*"
            self.keys[tag] = key

    def _get_path_for_tag(self, tag):
        if tag == "*":
            return self._keys_base_dir
        return self._keys_base_dir + tag

    def delete_key(self, tag):
        self._deleted_key_tags.append(tag)

    def add_key(self, tag, key):
        self.keys[tag] = key
        self._changed_key_tags.append(tag)

    def __str__(self):
        return "    %s = %s\n" % (self.access, self.name)
