from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)

from application import api
from application.api import RegGetUser, LogIn

api = Api(app)
api.add_resource(RegGetUser, '/users')
api.add_resource(LogIn, '/login')
#api.add_resource(UserAPI, '/user/<int:id>')