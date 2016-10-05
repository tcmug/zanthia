
import sys
import os
import subprocess
import tarfile
import string
import shutil
import yaml
import re

from DockerCompose import DockerComposeDriver


#
#   Class: BranchContainerException
#       BranchContainerException exception class.
#
class BranchContainerException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


#
#   Class: BranchContainer
#       BranchContainer class, "Manannan".
#
class BranchContainer:

    def create_from_branch(branch_name):
        return BranchContainer(None, None, None, branch_name)

    #
    #   Function: __init__
    #       Constructor
    #
    #   Parameters:
    #       self - Self
    #       tree_ish - Description
    #       old_commit - Description
    #       new_commit - Description
    #
    def __init__(self, tree_ish=None, old_commit=None,
                 new_commit=None, branch_name=None):

        self.tree_ish = tree_ish
        self.driver = None

        self.builds_location = os.environ.get(
            'ZANTHIA_BUILDS_DIR',
            '/var/git/app/'
        )

        self.remote_location = os.getcwd()

        self.repository_name = self.remote_location.split("/")[-1]
        self.repository_name = re.sub(r".git$", "", self.repository_name)

        if branch_name is None:

            self.branch_name = tree_ish.replace("refs/heads/", "")
            self.safe_branch_name = self.branch_name.replace("/", "__")

            # Determine the action to take based on commits.
            if old_commit == '0000000000000000000000000000000000000000':
                # Create the branch.
                self.action = 'create'
            elif new_commit == '0000000000000000000000000000000000000000':
                # Delete the branch.
                self.action = 'delete'
            else:
                # Otherwise, update.
                self.action = 'update'

        else:

            self.branch_name = branch_name
            self.safe_branch_name = self.branch_name.replace("/", "__")

        self.branch_archive = self.builds_location + \
            self.safe_branch_name + ".tar"

        self.branch_dir = "%s%s_%s" % (self.builds_location, self.repository_name, self.safe_branch_name)

        # But, if the branch does not exist yet, we have to create it.
        if not self.has_data():
            self.action = 'create'

    #
    #   Function: read_branch_yml
    #       Read branch specific yaml configuration.
    #
    #   Parameters:
    #       self - Self
    #       file - File to read under the branch directory
    #
    #   Returns:
    #       Configuration in dictionary form
    #
    def read_branch_yml(self, file):
        try:
            with open(self.get_directory() + "/" + file) as f:
                return yaml.safe_load(f)
        except:
            self.log("Problem reading from " + file)
        return {}

    #
    #   Function: write_branch_yaml
    #       Write branch specific yaml configuration.
    #
    #   Parameters:
    #       self - Self
    #       file - File to write to under the branch directory
    #       data - The data in dictionary form
    #
    def write_branch_yml(self, file, data):
        try:
            with open(self.get_directory() + "/" + file, 'w') as f:
                f.write('# Psst! This file was generated by Zanthia.\n')
                f.write(yaml.dump(data, default_flow_style=False))
        except:
            self.log("Problem writing to " + file)
        return {}

    #
    #   Function: get_directory
    #       Retreive the branch directory
    #
    #   Parameters:
    #       self - Self
    #
    #   Returns:
    #       Branch directory
    #
    def get_directory(self):
        return self.branch_dir

    #
    #   Function: has_data
    #       Check if the branch has data already
    #
    #   Parameters:
    #       self - Self
    #
    #   Returns:
    #       Boolean, True when branch has data, False if not.
    #
    def has_data(self):
        return os.path.isdir(self.branch_dir)

    #
    #   Function: log
    #       Log action
    #
    #   Parameters:
    #       self - Self
    #       msg - Message string
    #
    def log(self, msg):
        print "\033[92mManannan \033[0m" + msg
        sys.stdout.flush()

    #
    #   Function: prepare_driver
    #       Create and assign <Driver> to this branch.
    #
    #   Parameters:
    #       self - Description
    #
    def prepare_driver(self):

        if self.driver is not None:
            return

        self.settings = self.read_branch_yml("manannan.yml")

        if ('driver' in self.settings and
                self.settings['driver'] == 'DockerComposeDriver') or \
                self.driver is None:
            self.driver = DockerComposeDriver(self.settings)

        self.driver.set_branch_container(self)

    #
    #   Function: apply
    #       Apply the changes to the branch with the driver.
    #
    #   Parameters:
    #       self - Self
    #
    def apply(self):

        if not self.check():
            return

        self.log("preparing the " + self.action + " spell")

        # Apply the command.
        if self.action == 'create':
            self.create()
            self.prepare_driver()
            self.driver.clone()
            self.driver.start()

        elif self.action == 'update':
            self.prepare_driver()
            self.driver.stop()
            self.delete()
            self.create()
            self.driver.start()

        elif self.action == 'delete':
            self.prepare_driver()
            self.driver.stop()
            self.delete()

        self._notify_rest()

    #
    #   Function: delete
    #       Delete the branch. One of the steps invoken by apply().
    #
    #   Parameters:
    #       self - Self
    #
    def delete(self):
        # Delete the branch data if it exists.
        if os.path.isdir(self.branch_dir):
            shutil.rmtree(self.branch_dir)
            self.log('zapped branch container data')

    #
    #   Function: create
    #       Create the branch. One of the steps invoken by apply().
    #
    #   Parameters:
    #       self - Self
    #
    def create(self):
        # Use the archive command to create a tar of the branch HEAD
        # and untar it to a given directory. Finally remove the tar.
        self.git(
            "archive",
            "-o", self.branch_archive,
            "--remote", self.remote_location,
            self.branch_name + ":"
        )

        if os.path.isfile(self.branch_archive):
            tar = tarfile.open(self.branch_archive)
            tar.extractall(self.branch_dir)
            tar.close()
            os.remove(self.branch_archive)
            self.log('organized branch container data')
        else:
            raise BranchContainerException("Unable to archive")

    #
    #   Function: git
    #       Shorthand git function.
    #
    #   Parameters:
    #       self - Self
    #       *args - Git arguments
    #
    #   Returns:
    #       string - Results
    #
    def git(self, *args):
        return subprocess.call(['git'] + list(args))

    def check(self):
        return self.repository_name != "gitolite-admin"

    # x
    def _notify_rest(self):
        import requests
        requests.get('http://rest:8080/vhosts', auth=('zanthia', 'password'))
