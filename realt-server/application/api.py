from application import app
from flask_restful import Resource, reqparse, abort
from flask import jsonify
from application.db.database import db_session
from application.model.models import User
from sqlalchemy import and_
from hashlib import sha1

class RegGetUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('login', type=str, required=True, help="Login cannot be blank!")
            parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
            parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
            parser.add_argument('phone_number', type=str, required=True, help="Phone number cannot be blank!")
            parser.add_argument('firstname', type=str, required=True, help="Firstname cannot be blank!")
            parser.add_argument('lastname', type=str, required=True, help="Lastname cannot be blank!")
            parser.add_argument('birthday', type=str)
            args = parser.parse_args()

            new_user = User(login=args['login'],
                            password=sha1(args['password']).hexdigest(),
                            email=args['email'],
                            phone_number=args['phone_number'],
                            firstname=args['firstname'],
                            lastname=args['lastname'],
                            birthday=args['birthday'])

            db_session.add(new_user)
            db_session.commit()

            return {'success': 'User is created'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role', type=int)
        args = parser.parse_args()

        if args['role'] == 2: # admin
            users = {}
            for user in db_session.query(User).all():
                users.setdefault('users', []).append({'login': user.login,
                                                      'password': user.password,
                                                      'email': user.email,
                                                      'phone_number': user.phone_number,
                                                      'firstname': user.firstname,
                                                      'lastname': user.lastname,
                                                      'birthday': user.birthday,
                                                      'role': user.role,
                                                      'id': user.id})
        else:
            return {'Fail': 'You have no permissions to see information about users'}

        return jsonify(users)

class LogIn(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        login = args['login']
        password = args['password']

        user = db_session.query(User).filter(and_(User.login == login, User.password == password)).first()
        if user == None:
            abort(401, message='Login or password are incorrect!')
        else:
            return {'login': user.login,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'birthday': user.birthday,
                    'role': user.role}

class EditDeleteUser(Resource):
    def delete(self, id):
        user_to_delete = db_session.query(User).filter(User.id == id).first()
        if user_to_delete == None:
            return {'Fail': 'There is no user with such id!'}
        else:
            db_session.delete(user_to_delete)
            db_session.commit()

    def post(self, id):
        user = db_session.query(User).filter(User.id == id).first()
        if user == None:
            return {'Fail': 'There is no user with such id!'}
        else:
            try:
                parser = reqparse.RequestParser(bundle_errors=True)
                parser.add_argument('login', type=str, required=True, help="Login cannot be blank!")
                parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
                parser.add_argument('phone_number', type=str, required=True, help="Phone number cannot be blank!")
                parser.add_argument('firstname', type=str, required=True, help="Firstname cannot be blank!")
                parser.add_argument('lastname', type=str, required=True, help="Lastname cannot be blank!")
                parser.add_argument('birthday', type=str)
                #parser.add_argument('role', type=int)
                args = parser.parse_args()

                user.login = args['login']
                user.email = args['email']
                user.phone_number = args['phone_number']
                user.firstname = args['firstname']
                user.lastname = args['lastname']
                user.birthday = args['birthday']
                #user.role = args['role']
                db_session.add(user)
                db_session.commit()

                return jsonify({'Success' : 'User is updated.'})

            except Exception as e:
                return {'error': str(e)}

# remove database sessions at the end of the request or when the application shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


#To do:
#1. check if user exist - forbid registration with such credentials