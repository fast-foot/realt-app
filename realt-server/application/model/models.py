from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from application.db.database import Base, init_db

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    applications = relationship('Application', back_populates='user')
    login = Column(String(50))
    password = Column(String(40))
    email = Column(String(80))
    phone_number = Column(String(50))
    firstname = Column(String(50))
    lastname = Column(String(50))
    birthday = Column(String(20))
    role = Column(Integer) # 1 - user / 2 - admin

    def __init__(self, login, password, email, phone_number, firstname, lastname, birthday, role=1):
        self.login = login
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.role = role

    def __repr__(self):
        return "<User(login='%s', " \
            "password='%s', " \
            "email='%s', " \
            "phone_number='%s', " \
            "firstname='%s', " \
            "lastname='%s', " \
            "birthday='%s', " \
            "role='%s')>" % (self.login, self.password, self.email, self.phone_number,
                             self.firstname, self.lastname, self.birthday, self.role)

class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='applications')
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address', uselist=False, back_populates='application')
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='application')
    _type = Column(Integer) #sale / rent
    status = Column(Integer)
    add_date = Column(String(10))

    def __init__(self, _type, status, add_date):
        self._type = _type
        self.status = status
        self.add_date = add_date

    def __repr__(self):
        return "<Application(type='%s', " \
            "status='%s', " \
            "add_date='%s)>" % (self._type, self.status, self.add_date)


class PropertyType(Base):
    __tablename__ = 'property_types'

    id = Column(Integer, primary_key=True)
    properties = relationship('Property', back_populates='property_type')
    type_name = Column(String(20)) # house / flat / room

    def __init__(self, type_name):
        self.type_name = type_name

    def __repr__(self):
        return "<PropertyType(type_name='%s')>" % (self.type_name)


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    application = relationship('Application', uselist=False, back_populates='property') #one-to-one relation
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address', back_populates='property')
    property_type_id = Column(Integer, ForeignKey('property_types.id'))
    property_type = relationship('PropertyType', back_populates='properties')
    total_square = Column(Float)
    live_square = Column(Float)
    kitchen_square = Column(Float)
    price = Column(Float)
    year = Column(String(4))
    floor = Column(Integer)
    floors = Column(Integer)
    rooms_number = Column(Integer)
    description = Column(String(220))

    def __init__(self, total_square, live_square, kitchen_square, price,
                 year, floor, floors, rooms_number, description):
        self.total_square = total_square
        self.live_square = live_square
        self.kitchen_square = kitchen_square
        self.price = price
        self.year = year
        self.floor = floor
        self.floors = floors
        self.rooms_number = rooms_number
        self.description = description

    def __repr__(self):
        return "Property<(total_square='%s', " \
            "live_square='%s', " \
            "kitchen_square='%s', " \
            "price='%s', " \
            "year='%s', " \
            "floor='%s', " \
            "floors='%s', " \
            "rooms_number='%s', " \
            "description='%s')>" % (self.total_square, self.live_square,
                                    self.kitchen_square, self.price, self.year,
                                    self.floor, self.floors, self.rooms_number, self.description)


properties_features = Table('properties_features', Base.metadata,
            Column('property_id', ForeignKey('properties.id')),
            Column('feature_id', ForeignKey('features.id'))
)


class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Feature(name='%s')>" % (self.name)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    property = relationship('Property', uselist=False, back_populates='address')
    application = relationship('Application', back_populates='address')
    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship('Region', back_populates='addresses')
    address_type_id = Column(Integer, ForeignKey('address_types.id'))
    address_type = relationship('AddressType', back_populates='addresses')
    city = Column(String(80))
    street = Column(String(50))
    house_number = Column(String(10))

    def __init__(self, city, street, house_number):
        self.city = city
        self.street = street
        self.house_number = house_number

    def __repr__(self):
        return "Address<(city='%s', " \
            "street='%s', " \
            "house_number='%s')>" % (self.city, self.street, self.house_number)

class AddressType(Base):
    __tablename__ = 'address_types'

    id = Column(Integer, primary_key=True)
    addresses = relationship('Address', back_populates='address_type')
    street_type = Column(String(20))

    def __init__(self, street_type):
        self.street_type = street_type

    def __repr__(self):
        return "AdressType<(street_type='%s'>" % (self.street_type)

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    addresses = relationship('Address', back_populates='region')
    region_name = Column(String(70))

    def __init__(self, region_name):
        self.region_name = region_name

    def __repr__(self):
        return "<Region(region_name='%s')>" % (self.region_name)


init_db()