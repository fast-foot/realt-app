from flask import Flask
from flask_restful import Api
from application.db.database import db_session
from application.db.seed import main_seed
from application.model import models

#main_seed(db_session, models)

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