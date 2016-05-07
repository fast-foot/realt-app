# -*- coding: utf-8 -*-
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
    login = request.form['login'].encode('utf-8')
    password = request.form['password'].encode('utf-8')
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
        session['user_id'] = data['user_id']

        return render_template('index.html')
    else:
        return render_template('auth-fail.html')


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


@app.route('/send_application')
def send_application():
    req_url = rest_api() + '/application_data'
    r = requests.get(req_url)
    data = json.loads(r.text.encode('utf-8'))

    return render_template('application_form.html', data=data)


@app.route('/private', methods=['GET'])
def private():
    req_url = rest_api() + '/users?role=2'
    r = requests.get(req_url)
    data = json.loads(r.text)

    return render_template('edit_profile.html', userdata=data['users'])


@app.route('/admin_applications')
def admin_applications():
    req_url = rest_api() + '/applications'
    r = requests.get(req_url)
    data = json.loads(r.text)

    if data['app_count'] == 0:
        return render_template('admin_applications.html', empty_apps=True)

    return render_template('admin_applications.html',
                           applications=data['applications'],
                           applications_count=data['app_count'])


@app.route('/user_applications')
def user_applications():
    id = str(session['user_id'])
    req_url = rest_api() + '/applications/' + id

    r = requests.get(req_url)
    data = json.loads(r.text)

    if data['app_count'] == 0:
        return render_template('user_applications.html', empty_apps=True)

    return render_template('user_applications.html',
                           empty_apps=False,
                           applications=data['applications'],
                           applications_count=data['app_count'])


@app.route('/public_applications')
def public_applications():
    req_url = rest_api() + '/published_applications'
    r = requests.get(req_url)
    data = json.loads(r.text)

    if data['app_count'] == 0:
        return render_template('public_applications.html', empty_apps=True)

    req_url = rest_api() + '/application_data'
    r = requests.get(req_url)
    init_data = json.loads(r.text.encode('utf-8'))

    return render_template('public_applications.html',
                           empty_apps=False,
                           data=init_data,
                           applications=data['applications'],
                           applications_count=data['app_count'])