
from flask import Flask, abort, jsonify, request, make_response, render_template, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader

from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp
from wtforms.widgets import TextArea

import os

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'AAABBBBAAAA';

import Zanthia


class NewUserForm(Form):
#    select = SelectField('Something', choices=[('hello', 'abba'), ('hello', 'cell')])
    name = StringField('Name',
        validators=[
            DataRequired(),
            Regexp('^\w+$', message="Username must contain only letters numbers or underscore"),
        ]
    )
    pubkey_tag = StringField('Tag', validators=[DataRequired(),Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    pubkey = StringField('Public key', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Save')

class AddKeyForm(Form):
    pubkey_tag = StringField('Tag', validators=[DataRequired(),Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    pubkey = StringField('Public key', widget=TextArea(), validators=[DataRequired()])
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
@app.route('/users/<user>/<func>', methods=["GET", "POST"])
def users_page(user=False, func='list'):

    git = Zanthia.Gitolite()

    users = git.get_users()

    context = default_context()

    if user:

        # This is crap code.

        if user == 'new':
            user = Zanthia.GitoliteUser('')
            func = 'new'
        else:
            user = users[user]
            if func == 'list':
                func = 'edit'

        form = False

        if func == 'new':
            form = NewUserForm(obj=user)
        elif func == 'add':
            form = AddKeyForm(obj=user)
        else:
            abort(404, func)

        if form.validate_on_submit():

            form.populate_obj(user)
            user.save()

            return redirect(url_for('users_page'))

        context['form'] = form
        context['user'] = user

    context['func'] = func
    context['config'] = git.get_config()
    context['users'] = sorted(users.items())

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



@app.route('/js/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))


if __name__ == '__main__':
    app.run()
