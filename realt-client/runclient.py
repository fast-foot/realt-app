from application import app
from application.views import session

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=4992
    )