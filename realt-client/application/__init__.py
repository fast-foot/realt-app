import flask, os

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(24).encode('hex')

from application import views
