from flask import Flask
from flask_restful import Api

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

from application import api
from application.api import RegGetUser, LogIn, EditDeleteUser

api = Api(app)
api.add_resource(RegGetUser, '/users')
api.add_resource(LogIn, '/login')
api.add_resource(EditDeleteUser, '/user/<string:id>')