def check_application_filter(params):

    if params['price1'] and params['price2'] and params['city'] and params['street']:
        return 1

    elif not params['price1'] and not params['price2'] and not params['city'] and not params['street']:
        return 2

    elif params['price1'] and params['price2'] and not params['city']:
        return 3

    elif params['city'] and not params['price1'] and not params['price2'] and not params['street']:
        return 4

    elif params['city'] and params['street'] and not params['price1'] and not params['price2']:
        return 5

    elif params['city'] and not params['street'] and params['price1'] and params['price2']:
        return 6