
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'AAABBBBAAAA'

import Zanthia
import re

auth = HTTPBasicAuth()

auth_users = {
    "zanthia": "password",
    "internal": "password"
}

@auth.get_password
def get_pw(username):
    if username in auth_users:
        return auth_users[username]
    return None



re_name = re.compile('^\w+$')
re_group_name = re.compile('^@\w+$')
re_tag = re.compile('^\*|\w+$')


def validate_request_object(obj, reference):
    for key, pattern in reference.iteritems():
        if type(obj[key]) == unicode and not pattern.match(obj[key]):
            return False
    return True


@app.route('/')
@auth.login_required
def root():
    return jsonify({
        'result': [
            '/repositories',
            '/groups',
            '/users',
            '/vhosts'
        ]
    })


def docker_exec(params, capture = False):
    import subprocess
    import os
    import sys
    sys.stdout.flush()
    params.insert(1, "--host=unix:///tmp/docker.sock")
    params.insert(0, "sudo")
    if capture:
        proc = subprocess.Popen(params, env=os.environ.copy(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        retval, err = proc.communicate()
    else:
        retval = subprocess.call(params)
    return retval


@app.route('/vhosts/', methods=['GET'])
@auth.login_required
def proxies():

    response = {
        'status': 'ok',
    }

    vhost_path = '/etc/apache2/vhosts'

    if request.method == 'GET':

        from jinja2 import Environment, FileSystemLoader
        import json
        import os

        ids = str.splitlines(docker_exec(['docker', 'ps', '-q', '--filter=name=zzz'], capture = True))
        vhosts = []
        for container_id in ids:
            inspect = docker_exec(['docker', 'inspect', container_id], capture = True)
            inspect = json.loads(inspect)
            # print inspect[0]['Config']['Env']
            # print inspect[0]['NetworkSettings']['IPAddress']
            # print inspect[0]['Config']['ExposedPorts']
            container_env = dict(item.split("=", 1) for item in inspect[0]['Config']['Env'])

            if 'ZANTHIA_HTTP_PORT' in container_env:
                servername = "%s.%s" % (inspect[0]['Name'][4:], os.getenv('ZANTHIA_SERVERNAME', 'localhost'))
                vhosts.append({
                    'servername': "%s" % (servername),
                    'url': "http://%s:%s/" % (
                        inspect[0]['NetworkSettings']['Networks']['zanthia_zanthia']['IPAddress'],
                        container_env['ZANTHIA_HTTP_PORT']
                    )
                });

        config = ""

        j2_env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True)

        for vhost in vhosts:
            content = j2_env.get_template('vhost.conf.j2').render(vhost)
            config = config + content

        # from os import listdir
        # from os.path import isfile, join, splitext
        # vhosts = [splitext(f)[0] for f in listdir(vhost_path) if isfile(join(vhost_path, f))]
        with open('%s/zanthia.conf' % (vhost_path), 'w+') as file:
            file.write(config)

        return jsonify({
            'result': vhosts
        })



@app.route('/repositories/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def repositories():

    response = {
        'status': 'ok',
    }

    if request.method == 'GET':

        git = Zanthia.Git()
        result = []
        for repo in git.get_repositories():
            result.append({
                'name': repo.name,
                'access': repo.access,
            })
        return jsonify({
            'result': result
        })

    elif request.method == 'PUT':

        git = Zanthia.Git()
        repo_data = request.get_json(silent=True)

        if validate_request_object(repo_data, { 'name': re_name }):
            new_repository = Zanthia.Repository(repo_data)
            git.add_repo(new_repository)
            git.save()
        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    return jsonify(response)


@app.route('/groups/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def groups():
    response = {
        'status': 'ok',
    }

    if request.method == 'GET':

        git = Zanthia.Git()
        result = []
        for group in git.get_groups():
            result.append({
                'name': group.name,
                'users': group.users
            })

        return jsonify({
            'result': result
        })

    elif request.method == 'PUT':

        git = Zanthia.Git()
        group_data = request.get_json(silent=True)

        if validate_request_object(group_data, { 'name': re_group_name }):

            new_group = Zanthia.Group(group_data)
            git.add_group(new_group)
            git.save()

        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    elif request.method == 'DELETE':

        git = Zanthia.Git()
        group_data = request.get_json(silent=True)

        if validate_request_object(group_data, { 'name': re_group_name }):

            git.delete_group(group_data['name'])
            git.save()

        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    else:
        response.status = 'error'

    return jsonify(response)



@app.route('/users/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def users():

    response = {
        'status': 'ok',
    }

    if request.method == 'GET':

        git = Zanthia.Git()
        result = []

        for user in git.get_users():

            result.append({
                'name': user.name,
                'keys': user.keys
            })

        response['result'] = result

    elif request.method == 'PUT':

        git = Zanthia.Git()
        user_data = request.get_json(silent=True)
        if validate_request_object(user_data, { 'name': re_name, 'tag': re_tag }):
            new_user = Zanthia.User(user_data['name'])
            new_user.add_key(user_data['tag'], user_data['key'])
            new_user.save()
            git.save()
            response['status'] = 'ok'
        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    elif request.method == 'DELETE':

        git = Zanthia.Git()
        user_data = request.get_json(silent=True)
        if 'name' in user_data and 'tag' in user_data:
            new_user = Zanthia.User(user_data['name'])
            new_user.delete_key(user_data['tag'])
            new_user.save()
            git.save()
            response['status'] = 'ok'
        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    else:
        response.status = 'error'

    return jsonify(response)



if __name__ == '__main__':
    app.run()
