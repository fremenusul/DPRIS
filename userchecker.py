import checker


def getuser(user):
    if user:
        user_email = user.email()
        auth = checker.isIC(user_email)
    else:
        auth = False, 'N/A'
    if auth[0] is True:
        auth_ic = True
    else:
        auth_ic = False
    return auth_ic


def getuserplatoon(user):
    if user:
        user_email = user.email()
        auth = checker.isIC(user_email)
    else:
        auth = False, 'N/A'
    if auth[0] is True:
        auth_ic = True
        auth_platoon = auth[1]
    else:
        auth_ic = False
        auth_platoon = 'N/A'
    return auth_ic, auth_platoon
