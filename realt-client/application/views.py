from application import app
from flask import render_template, request, session
#from flask.ext.session import Session
from application.config import rest_api
from hashlib import sha1
import json, requests

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404

@app.route('/', methods=['POST'])
def login_user():
    login = request.form['login']
    password = request.form['password']
    password = sha1(password).hexdigest()

    req_url = rest_api() + '/login?' + 'login=' + login + '&password=' + password
    r = requests.get(req_url)

    if r.status_code == 200:
        data = json.loads(r.text)
        session['login'] = str(login)
        session['email'] = data['email']
        session['firstname'] = data['firstname']
        session['lastname'] = data['lastname']
        session['birthday'] = data['birthday']
        session['role'] = data['role']

        return render_template('index.html')
    else:
        a = r.content
        return  render_template('index.html', not_auth=r.content)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    req_url = rest_api() + '/users?role=' + str(session['role'])
    r = requests.get(req_url)
    data = json.loads(r.text)

    return render_template('users.html', users=data['users'])

