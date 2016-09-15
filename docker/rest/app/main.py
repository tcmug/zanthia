
from flask import Flask, jsonify, request
from flask_digest import Stomach

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'AAABBBBAAAA'
stomach = Stomach('Zanthia')

import Zanthia
import re

rest_users = {}


@stomach.register
def add_user(username, password):
    rest_users[username] = password


@stomach.access
def get_pw(username):
    if username in rest_users:
        return rest_users[username]
    return None


add_user("zanthia", "password")

re_name = re.compile('^\w+$')
re_group_name = re.compile('^@\w+$')
re_tag = re.compile('^\*|\w+$')


def validate_request_object(obj, reference):
    for key, pattern in reference.iteritems():
        if type(obj[key]) == unicode and not pattern.match(obj[key]):
            return False
    return True


@app.route('/')
@stomach.protect
def root():
    print request.headers
    return jsonify({
        'result': [
            '/repositories',
            '/groups',
            '/users'
        ]
    })


@app.route('/repositories/', methods=['GET', 'PUT', 'DELETE'])
@stomach.protect
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
@stomach.protect
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
@stomach.protect
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
            response['status'] = 'ok'
        else:
            response['status'] = 'error'
            response['message'] = 'malformed object'

    else:
        response.status = 'error'

    return jsonify(response)



if __name__ == '__main__':
    app.run()
