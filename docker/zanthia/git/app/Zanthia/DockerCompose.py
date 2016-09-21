
import sys
import os
import subprocess
import tarfile
import string
import shutil
import yaml
import json

from Driver import DriverBase


#
#   Class: DockerComposeDriver
#       DockerComposeDriver, "Gwydion". Extends <Driver>.
#
class DockerComposeDriver(DriverBase):

    #
    #   Function: __init__
    #       Description
    #
    #   Parameters:
    #       self - Description
    #       settings - Description
    #
    #   Returns:
    #       def
    #
    def __init__(self, settings):
        self.env_vars = False
        self.name = "Gwydion"
        self.machine_name = 'default'
        self.settings = settings

    #
    #   Function: _get_environment_vars
    #       Description
    #
    #   Parameters:
    #       self - Description
    #
    #   Returns:
    #       def
    #
    def _get_environment_vars(self):
        if not self.env_vars:
            # out = subprocess.check_output([
            #     'docker-machine',
            #     'env',
            #     self.machine_name]
            # )
            # env = string.split(out, '\n')

            # env = [
            #     ln.replace('export ', '').replace('"', '')
            #     for ln in env if 'export ' in ln
            # ]
            # env = dict(keyvalue.split('=') for keyvalue in env)

            #self.env_vars = env.update(os.environ.copy())
            self.env_vars = os.environ.copy()
            #self.env_vars["DOCKER_HOST"] = "unix:///tmp/docker.sock"
        return self.env_vars

    #
    #   Function: clone
    #       Description
    #
    #   Parameters:
    #       self - Description
    #
    #   Returns:
    #       def
    #
    def clone(self):

        compose = self.branch_container.read_branch_yml("docker-compose.yml")

        # First bring up the containers in order to create them:
        self.build()
        # self.stop()

        # ADD: Stop source services

        # Then loop through the containers in order to clone the data in them:
        for container_name, source_branch in self.settings['clone-source'].iteritems():
            if source_branch != self.branch_container.branch_name:

                self._stop_container(source_branch, container_name)

                source_container_id = source_branch \
                    + "_" + container_name \
                    + "_1"

                target_container_id = self.branch_container.branch_name \
                    + "_" \
                    + container_name + "_1"

                self.docker_clone_volumes(
                    source_container_id,
                    target_container_id
                )

                self._start_container(source_branch, container_name)

                # self.log("Cloning finished, starting " + container_name)
                # self.shell_exec(['docker-compose', 'start', container_name])

                # if container_name in compose:
                #   if 'build' in compose[container_name]:
                #       compose[container_name].pop("build", None)
                #   compose[container_name]['image'] = target_container_id.strip()

        # ADD: Start source services

        # self.branch_container.write_branch_yml("docker-compose.yml", compose)

        # load clone-source, for each source
        #   create a commit from source:
        #   $ docker commit -m "Testing" originbranch_source_1
        #   in docker-compose.yml, replace sources image with
        #   newly generated image hash

    #
    #   Function: start
    #       Description
    #
    #   Parameters:
    #       self - Description
    #
    #   Returns:
    #       def
    #
    def start(self):
        if self.branch_container.has_data():
            self.log('waking up services')
            self.shell_exec([
                'docker-compose',
                '-p' + self._get_docker_compose_name(),
                'up',
                '-d'
            ])
            #  '--no-recreate'


    def _start_container(self, branch, name):
        self.log("Stopping " + branch + " " + name + "...")
        self.shell_exec([
            'docker-compose',
            '-p' + self._get_docker_compose_name(branch),
            'start',
            name
        ])


    def _stop_container(self, branch, name):
        self.log("Stopping " + branch + " " + name + "...")
        self.shell_exec([
            'docker-compose',
            '-p' + self._get_docker_compose_name(branch),
            'stop',
            name
        ])


    def _get_docker_compose_name(self, branch = None):

        if branch is None:
            return "%s_%s" % (
                self.branch_container.repository_name,
                self.branch_container.safe_branch_name
            )

        return "%s_%s" % (
            self.branch_container.repository_name,
            branch
        )



    #
    #   Function: stop
    #       Description
    #
    #   Parameters:
    #       self - Description
    #
    #   Returns:
    #       def
    #
    def build(self):
        if self.branch_container.has_data():
            self.log('building services')
            self.shell_exec([
                'docker-compose',
                'build'
            ])
            self.start()
            self.stop()

    #
    #   Function: stop
    #       Description
    #
    #   Parameters:
    #       self - Description
    #
    #   Returns:
    #       def
    #
    def stop(self):
        if self.branch_container.has_data():
            self.log('putting services to bed')
            self.shell_exec([
                'docker-compose',
                '-p' + self._get_docker_compose_name(),
                'stop'
            ])

    #
    #   Function: shell_exec
    #       Description
    #
    #   Parameters:
    #       self - Description
    #       params - Description
    #       False - Description
    #
    #   Returns:
    #       def
    #
    def shell_exec(self, params, capture = False):
        prev_dir = os.getcwd()
        sys.stdout.flush()
        os.chdir(self.branch_container.get_directory())
        params.insert(1, "--host=unix:///tmp/docker.sock")
        params.insert(0, "sudo")
        print " ".join(params)
        if capture:
            proc = subprocess.Popen(params, env=self._get_environment_vars(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            retval, err = proc.communicate()
            # print(retval)
            # print(err)
        else:
            retval = subprocess.call(params, env=self._get_environment_vars())
            os.chdir(prev_dir)
        return retval

    #
    #   Function: docker_clone_volumes
    #       Description
    #
    #   Parameters:
    #       self - Description
    #       source_container_id - Description
    #       target_container_id - Description
    #
    #   Returns:
    #       def
    #
    def docker_clone_volumes(self, source_container_id, target_container_id):

        inspect = self.shell_exec(['docker', 'inspect', source_container_id], capture = True)
        inspect = json.loads(inspect)

        if 0 < len(inspect) \
           and 'Mounts' in inspect[0]:

            self.log("Starting cloning process from " + source_container_id + " to " + target_container_id)

            for mount in inspect[0]['Mounts']:
                source = mount['Destination']

                self.log("Copying " + source + " from " + source_container_id + " to " + target_container_id)

                self.shell_exec([
                    "docker",
                    "run",
                    "--volumes-from", source_container_id,
                    "-v", "/tmp:/backup",
                    "busybox",
                    "tar", "cvf", "/backup/export.tar", source
                ], capture=True)
                # docker run --volumes-from master_database_1 -v $(pwd):/backup debian tar cvf /backup/backup.tar /var/lib/mysql

                self.shell_exec([
                    "docker",
                    "run",
                    "--volumes-from", target_container_id,
                    "-v", "/tmp:/backup",
                    "busybox",
                    "tar", "xvf", "/backup/export.tar"
                ], capture=True)
                # docker run --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar"
        else:

            self.log("Nothing to clone from " + source_container_id + " to " + target_container_id)




