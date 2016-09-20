
from flask import Flask, jsonify, request

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True
app.config['SECRET_KEY'] = 'AAABBBBAAAA'

import Zanthia
import re

auth = HTTPBasicAuth()

auth_users = {
    "zanthia": "password",

@app.route('/')
@auth.login_required
def root():
    return jsonify({
        'implement': 'me'
    })



