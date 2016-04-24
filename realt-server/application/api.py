# coding: utf-8
from application import app
from flask_restful import Resource, reqparse, abort
from flask import jsonify
from application.db.database import db_session
from application.model.models import User, PropertyType, Region, AddressType, Feature
from sqlalchemy import and_, desc
from hashlib import sha1


class RegGetUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('login', required=True, help="Login cannot be blank!")
            parser.add_argument('password', required=True, help="Password cannot be blank!")
            parser.add_argument('email', required=True, help="Email cannot be blank!")
            parser.add_argument('phone_number', required=True, help="Phone number cannot be blank!")
            parser.add_argument('firstname', required=True, help="Firstname cannot be blank!")
            parser.add_argument('lastname', required=True, help="Lastname cannot be blank!")
            parser.add_argument('birthday')
            args = parser.parse_args()

            check_exist_user = db_session.query(User).filter(User.login == args['login'].encode('utf-8')).first()
            if check_exist_user == None:
                new_user = User(login=args['login'].encode('utf-8'),
                                password=sha1(args['password'].encode('utf-8')).hexdigest(),
                                email=args['email'].encode('utf-8'),
                                phone_number=args['phone_number'].encode('utf-8'),
                                firstname=args['firstname'].encode('utf-8'),
                                lastname=args['lastname'].encode('utf-8'),
                                birthday=args['birthday'].encode('utf-8'))

                db_session.add(new_user)
                db_session.commit()

                return {'success': 'true', 'message': 'User is created.'}

            else:
                return {'success': 'false', 'message': 'User with such login already exist.'}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role', type=int)
        args = parser.parse_args()

        if args['role'] == 2: # admin
            users = {}
            for user in db_session.query(User).order_by(desc(User.role)).all():
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
        parser.add_argument('login', required=True)
        parser.add_argument('password', required=True)
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
        ids_list = id.strip().split(",")

        for id in ids_list:
            user = db_session.query(User).filter(User.id == int(id)).first()
            db_session.delete(user)
            db_session.commit()

        return {'msg': 'Users have been deleted.'}

    def put(self, id):
        user = db_session.query(User).filter(User.id == int(id)).first()
        if user == None:
            return {'Fail': 'There is no user with such id!'}
        else:
            try:
                parser = reqparse.RequestParser(bundle_errors=True)
                parser.add_argument('login',required=True, help="Login cannot be blank!")
                parser.add_argument('email', required=True, help="Email cannot be blank!")
                parser.add_argument('phone_number', required=True, help="Phone number cannot be blank!")
                parser.add_argument('firstname', required=True, help="Firstname cannot be blank!")
                parser.add_argument('lastname', required=True, help="Lastname cannot be blank!")
                parser.add_argument('birthday', type=str)
                parser.add_argument('role', type=int)
                args = parser.parse_args()

                user.login = args['login'].encode('utf-8')
                user.email = args['email'].encode('utf-8')
                user.phone_number = args['phone_number'].encode('utf-8')
                user.firstname = args['firstname'].encode('utf-8')
                user.lastname = args['lastname'].encode('utf-8')
                user.birthday = args['birthday'].encode('utf-8')
                user.role = args['role']
                db_session.add(user)
                db_session.commit()

                return jsonify({'Success' : 'User is updated.'})

            except Exception as e:
                return {'error': str(e)}


class AddGetDeleteEditApplication(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser(bundle_errors=True)
            parser.add_argument('login', required=True, help="Login cannot be blank!")
            parser.add_argument('password', required=True, help="Password cannot be blank!")
            parser.add_argument('email', required=True, help="Email cannot be blank!")
            parser.add_argument('phone_number', required=True, help="Phone number cannot be blank!")
            parser.add_argument('firstname', required=True, help="Firstname cannot be blank!")
            parser.add_argument('lastname', required=True, help="Lastname cannot be blank!")
            parser.add_argument('birthday')
            args = parser.parse_args()

        except Exception as e:
            return {'error': str(e)}


class DataForApplication(Resource):
    def get(self):
        data = {}
        property_types = []
        regions = []
        address_types = []
        features = []

        for prop_type in db_session.query(PropertyType).order_by(PropertyType.id).all():
            property_types.append({
                "type": prop_type.type_name.encode('utf-8'),
                "id": prop_type.id
            })

        for region in db_session.query(Region).order_by(Region.id).all():
            regions.append({
                "name": region.region_name,
                "id": region.id
            })

        for address_type in db_session.query(AddressType).order_by(AddressType.id).all():
            address_types.append({
                "street_type": address_type.street_type,
                "id": address_type.id
            })

        for feature in db_session.query(Feature).order_by(Feature.id).all():
            features.append({
                "name": feature.name,
                "id": address_type.id
            })

        data['property_types'] = property_types
        data['regions'] = regions
        data['address_types'] = address_types
        data['features'] = features

        return jsonify(data)


# remove database sessions at the end of the request or when the application shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()