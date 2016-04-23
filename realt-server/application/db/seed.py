# coding: utf-8
def seed_regions(db_session, Region):
    regions = list()
    regions.append(Region(region_name='Минская'))
    regions.append(Region(region_name='Могилевская'))
    regions.append(Region(region_name='Брестская'))
    regions.append(Region(region_name='Гродненская'))
    regions.append(Region(region_name='Гомельская'))
    regions.append(Region(region_name='Витебская'))

    db_session.add_all(regions)
    db_session.commit()


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

    db_session.add_all(features)
    db_session.commit()

