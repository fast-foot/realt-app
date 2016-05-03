def check_application_filter(params):

    if params['price1'] and params['price2'] and params['city']:
        return 1

    elif not params['price1'] and not params['price2'] and not params['city']:
        return 2

    elif params['price1'] and params['price2'] and not params['city']:
        return 3

    else:
        return 4
