# coding: utf-8
from hashlib import sha1


def seed_regions(db_session, Region):
    regions = list()
    regions.append(Region(region_name='Минская'))
    regions.append(Region(region_name='Могилевская'))
    regions.append(Region(region_name='Брестская'))
    regions.append(Region(region_name='Гродненская'))
    regions.append(Region(region_name='Гомельская'))
    regions.append(Region(region_name='Витебская'))

    return regions


def seed_features(db_session, Feature):
    features = list()
    features.append(Feature(name='Холодильник'))
    features.append(Feature(name='Телевизор'))
    features.append(Feature(name='Интернет'))
    features.append(Feature(name='Плита'))
    features.append(Feature(name='Микроволновка'))
    features.append(Feature(name='Стиральная машина'))
    features.append(Feature(name='Ванна'))
    features.append(Feature(name='Балкон'))
    features.append(Feature(name='Мебель'))
    features.append(Feature(name='Кондиционер'))

    return features


def seed_address_type(db_session, AddressType):
    address_types = list()
    address_types.append(AddressType(street_type='Улица'))
    address_types.append(AddressType(street_type='Проспект'))
    address_types.append(AddressType(street_type='Переулок'))

    return address_types


def seed_property_type(db_session, PropertyType):
    property_types = list()
    property_types.append(PropertyType(type_name='Квартира'))
    property_types.append(PropertyType(type_name='Дом'))
    property_types.append(PropertyType(type_name='Комната'))

    return property_types


def seed_users(db_session, User):
    users = list()

    users.append(User(login='admin',
                      password=sha1('admin').hexdigest(),
                      email='admin@gmail.com',
                      phone_number='375297778899',
                      firstname='Alex',
                      lastname='Chudovsky',
                      birthday='23.11.1995',
                      role=2
                      )
    )

    for i in range(1, 21):
        users.append(User(login='User'+str(i),
                          password=sha1(str(i)).hexdigest(),
                          email='u'+str(i)+'@mail.com',
                          phone_number='37529123456'+str(i),
                          firstname='uName'+str(i),
                          lastname='uLastName'+str(i),
                          birthday=str(i)+'.'+str(i)+'.19'+str(80+i),
                          role=1
                          )
        )

    return users


def main_seed(db_session, models):
    db_session.add_all(seed_users(db_session, models.User))
    db_session.add_all(seed_regions(db_session, models.Region))
    db_session.add_all(seed_features(db_session, models.Feature))
    db_session.add_all(seed_address_type(db_session, models.AddressType))
    db_session.add_all(seed_property_type(db_session, models.PropertyType))

    db_session.commit()