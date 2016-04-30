from flask import Flask
from flask_restful import Api
from application.db.database import db_session
from application.db.seed import main_seed
from application.model import models
import sys
#main_seed(db_session, models)

app = Flask(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.headers.add('content-type', 'charset=utf-8')
  return response



from application import api
from application.api import RegGetUser, LogIn, EditDeleteUser, DataForApplication, AddGetDeleteEditApplication
from application.api import GetApplications

api = Api(app)
api.add_resource(RegGetUser, '/users')
api.add_resource(LogIn, '/login')
api.add_resource(EditDeleteUser, '/user/<string:id>')
api.add_resource(DataForApplication, '/application_data')
api.add_resource(AddGetDeleteEditApplication, '/application')
api.add_resource(GetApplications, '/applications')