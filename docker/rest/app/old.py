
from flask import Flask, abort, jsonify, request, make_response, render_template, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader

from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea

import os

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'AAABBBBAAAA';

import Zanthia


class UserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    pubkey = StringField('Public key', widget=TextArea(), validators=[DataRequired()])
#    select = SelectField('Something', choices=[('hello', 'abba'), ('hello', 'cell')])
    submit = SubmitField('Save')


def default_context():
    return {
        'mainnav': [
            { 'page': 'repositories', 'name': 'Repositories' },
            { 'page': 'groups', 'name': 'Groups' },
            { 'page': 'users', 'name': 'Users' }
        ]
    }

@app.route('/users', methods=["GET", "POST"])
@app.route('/users/<user>', methods=["GET", "POST"])
def users_page(user=False):

    git = Zanthia.Gitolite()

    users = git.get_users()

    if user:
        user = users[user]

    form = UserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        return redirect(url_for('users_page'))

    context = default_context()

    context['form'] = form
    context['config'] = git.get_config()
    context['repositories'] = git.get_repositories()
    context['groups'] = git.get_groups()
    context['users'] = users
    context['user'] = user

    return render_template('pages/users.html', **context)


@app.route('/')
@app.route('/<page>')
def root(page='repositories'):

    if page not in ['repositories', 'groups']:
        abort(404)

    git = Zanthia.Gitolite()

    context = {
        'config': git.get_config(),
        'repositories': git.get_repositories(),
        'groups': git.get_groups(),
        'users': git.get_users(),
        'page': page,
        'mainnav': [
            { 'page': 'repositories', 'name': 'Repositories' },
            { 'page': 'groups', 'name': 'Groups' },
            { 'page': 'users', 'name': 'Users' }
        ]
    }

    return render_template("pages/%s.html" % (page), **context)



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
