# coding: utf-8
from application import app
from flask_restful import Resource, reqparse, abort
from flask import jsonify
from application.db.database import db_session
from application.model.models import User, Property, PropertyType, Region, Address, AddressType, Feature, Application
from sqlalchemy import and_, desc
from hashlib import sha1
from application import util
import json


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
                    'role': user.role,
                    'user_id': user.id
                    }


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


class AddApplication(Resource):
    def post(self):
        try:
            #empty can be: floor, live_square, kitchen_square because of disabling on client
            parser = reqparse.RequestParser()
            parser.add_argument('applicationType', type=str)
            parser.add_argument('propertyType', type=str)
            parser.add_argument('city', type=str)
            parser.add_argument('region', type=str)
            parser.add_argument('street_type', type=str)
            parser.add_argument('street', type=str)
            parser.add_argument('house_number', type=str)
            parser.add_argument('total_square', type=str)
            parser.add_argument('live_square', type=str)
            parser.add_argument('kitchen_square', type=str)
            parser.add_argument('floor', type=str)
            parser.add_argument('floors', type=str)
            parser.add_argument('rooms_number', type=str)
            parser.add_argument('year', type=str)
            parser.add_argument('price', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('user_id', type=str)
            parser.add_argument('feature', action='append')
            args = parser.parse_args()

            address = Address(city=args['city'].encode('utf-8'),
                              street=args['street'].encode('utf-8'),
                              house_number=args['house_number'].encode('utf-8'))

            address.region_id = int(args['region'].encode('utf-8'))
            address.address_type_id = int(args['street_type'].encode('utf-8'))

            _property = Property(total_square=args['total_square'].encode('utf-8'),
                                 price=args['price'].encode('utf-8'),
                                 year=args['year'].encode('utf-8'),
                                 floors=int(args['floors'].encode('utf-8')),
                                 rooms_number=int(args['rooms_number'].encode('utf-8')),
                                 description=args['description'].encode('utf-8')
            )

            _property.live_square = float(args['live_square'].encode('utf-8')) if args['live_square'] is not None else -1
            _property.kitchen_square = float(args['kitchen_square'].encode('utf-8')) if args['kitchen_square'] is not None else -1
            _property.floor = int(args['floor'].encode('utf-8')) if args['floor'] is not None else -1

            _property.address = address
            _property.property_type_id = int(args['propertyType'].encode('utf-8'))

            application = Application(_type=args['applicationType'].encode('utf-8'))
            application.user_id = args['user_id'].encode('utf-8')
            application.address = address
            application.property = _property

            if args['feature'] is not None:
                for feature_id in args['feature']:
                    feature = db_session.query(Feature).filter(Feature.id == int(feature_id)).first()
                    db_session.add(feature)
                    _property.features.append(feature)

            db_session.add(address)
            db_session.add(_property)
            db_session.commit()

            return {'success': True, 'message': 'Application has been added.'}

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
                "id": feature.id
            })

        data['property_types'] = property_types
        data['regions'] = regions
        data['address_types'] = address_types
        data['features'] = features

        return jsonify(data)


class GetEditDeleteApplications(Resource):
    def get(self):
        applications = {}
        for application in db_session.query(Application).order_by(desc(Application.created_date)).all():

            address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
            )

            applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address
            })

        return jsonify(applications)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('app_ids', type=str)
        args = parser.parse_args()

        ids_list = args['app_ids'].strip().split(",")

        for id in ids_list:
            application = db_session.query(Application).filter(Application.id == int(id)).first()
            db_session.delete(application)

        db_session.commit()

        return {'msg': 'Applications have been deleted.'}

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('app_ids', type=str)
        parser.add_argument('app_status', type=int)
        args = parser.parse_args()

        ids_list = args['app_ids'].strip().split(",")
        app_status = args['app_status']

        for id in ids_list:
            application = db_session.query(Application).filter(Application.id == int(id)).first()
            application.status = app_status

        db_session.commit()

        return {'msg': 'Status of applications have been changed.'}


class GetApplications(Resource):
    def get(self, id):
        user_applications = {}

        for application in db_session.query(Application)\
                .filter(Application.user_id == int(id))\
                .order_by(desc(Application.created_date)).all():

            user_applications.setdefault('applications', []).append({
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id
            })

        return jsonify(user_applications)


class GetEditApplication(Resource):

    def get(self, id):

        application = db_session.query(Application).filter(Application.id == id).first()

        address = "{region} область, г. {city}, {street_type} {street}, дом {house_number}".format(
            region=application.address.region.region_name,
            city=application.address.city,
            street_type=application.address.address_type.street_type,
            street=application.address.street,
            house_number=application.address.house_number
        )

        purpose = "Аренда" if application._type == "rent" else "Продажа"

        features = []
        for feature in application.property.features:
            features.append(feature.name)

        return jsonify({
            'Цель': purpose,
            'Собственность': application.property.property_type.type_name,
            'Адрес': address,
            'Площадь общая': application.property.total_square,
            'Площадь жилая': application.property.live_square,
            'Площадь кухни': application.property.kitchen_square,
            'Этаж': application.property.floor,
            'Этажность': application.property.floors,
            'Кол-во комнат': application.property.rooms_number,
            'Год постройки': application.property.year,
            'Цена': application.property.price,
            'Описание': application.property.description,
            'Удобства': features
        })


class GetPublishedApplications(Resource):
    def get(self):
        applications = {}
        for application in db_session.query(Application)\
                .filter(Application.status == 1) \
                .order_by(desc(Application.created_date))\
                .all():

            address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
            )

            applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address,
                'price': application.property.price
            })

        return jsonify(applications)


class FilterApplications(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price1', type=str)
        parser.add_argument('price2', type=str)
        parser.add_argument('applicationType', type=str)
        parser.add_argument('propertyType', type=str)
        parser.add_argument('city', type=str)
        args = parser.parse_args()

        query_state = util.check_application_filter(args)
        applications = {}

        if query_state == 1:
            for application in db_session.query(Application)\
                .join(Application.property)\
                .join(Property.property_type)\
                .join(Application.address)\
                .filter(and_(Property.price <= float(args['price2']), Property.price >= float(args['price1'])))\
                .filter(PropertyType.id == int(args['propertyType']))\
                .filter(Application._type == args['applicationType'])\
                .filter(Address.city == args['city'].encode('utf-8'))\
                .filter(Application.status == 1)\
                .order_by(desc(Application.created_date))\
                .all():

                address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
                )

                applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address,
                'price': application.property.price
            })

        if query_state == 2:
            for application in db_session.query(Application)\
                .join(Application.property)\
                .join(Property.property_type)\
                .filter(PropertyType.id == args['propertyType'])\
                .filter(Application._type == args['applicationType'])\
                .filter(Application.status == 1)\
                .order_by(desc(Application.created_date))\
                .all():

                address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
                )

                applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address,
                'price': application.property.price
            })

        if query_state == 3:
            for application in db_session.query(Application)\
                .join(Application.property)\
                .join(Property.property_type)\
                .filter(and_(Property.price <= float(args['price2']), Property.price >= float(args['price1'])))\
                .filter(PropertyType.id == args['propertyType'])\
                .filter(Application._type == args['applicationType'])\
                .filter(Application.status == 1)\
                .order_by(desc(Application.created_date))\
                .all():

                address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
                )

                applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address,
                'price': application.property.price
            })

        if query_state == 4:
            for application in db_session.query(Application)\
                .join(Application.property)\
                .join(Property.property_type)\
                .join(Application.address)\
                .filter(PropertyType.id == args['propertyType'])\
                .filter(Application._type == args['applicationType'])\
                .filter(Address.city == args['city'].encode('utf-8'))\
                .filter(Application.status == 1)\
                .order_by(desc(Application.created_date))\
                .all():

                address = "г. {city}, {street_type} {street}".format(
                        city=application.address.city,
                        street_type=application.address.address_type.street_type,
                        street=application.address.street,
                )

                applications.setdefault('applications', []).append({
                'publisher': application.user.lastname + ' ' + application.user.firstname,
                'status': application.status,
                'created_date': application.created_date,
                'type': application._type,
                'property_type': application.property.property_type.type_name,
                'id': application.id,
                'phone_number': application.user.phone_number,
                'address': address,
                'price': application.property.price
            })

        return jsonify(applications)



# remove database sessions at the end of the request or when the application shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()