
from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader

import os

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True

import Zanthia

@app.route('/')
def root():

    git = Zanthia.Gitolite()

    context = {
        'config': git.get_config(),
        'repos': git.get_repositories(),
        'groups': git.get_groups(),
        'users': git.get_users()
    }

    return render_template("index.html", **context)

@app.route('/ajax/repositories')
def repositories():
    git = Zanthia.Gitolite()
    list = []
    for x in git.get_repositories():
        list.append(x.name)
    return jsonify(list)


@app.route('/ajax/repository/<repository>')
def repository(repository):
    git = Zanthia.Gitolite()
    list = [ 'blah' ]
    return jsonify(list)


@app.route('/ajax/user/<user>')
def user(user):
    git = Zanthia.Gitolite()
    list = []
    for x in git.get_groups():
        list.append(x.name)
    list.append(user)
    return jsonify(list)


@app.route('/ajax/groups')
def groups():
    git = Zanthia.Gitolite()
    list = []
    for x in git.get_groups():
        list.append(x.name)
    return jsonify(list)


@app.route('/js/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))


if __name__ == '__main__':
    app.run()
