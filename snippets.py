import ast
import datetime
from datetime import date

from google.appengine.ext import ndb

import models


def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m - 1, 12)
    return date(y + a, m + 1, 1)


# TODO(Shangpo) REMOVE BEFORE LIVE
def updatemodel():
    s_query = models.SoldierData.query(models.SoldierData.platoon == 'viking')
    soldier_data = s_query.fetch()

    for x in soldier_data:
        soldier_key = ndb.Key(urlsafe=x.key.urlsafe())
        soldier = soldier_key.get()
        soldier.num_certs = 0
        soldier.num_ribbons = 0
        soldier.num_badges = 0
        soldier.num_medals = 0
        soldier.num_awards = 0
        soldier.put()


def updatemodel2():
    e = models.AttendanceChecker(
        datecheck=datetime.date(2017, 5, 29),
        platoon='viking',
        attend=1)
    e.put()


def updatemodel3():
    s_query = models.SoldierData.query(models.SoldierData.platoon == 'viking')
    soldier_data = s_query.fetch()

    for x in soldier_data:
        soldier_key = ndb.Key(urlsafe=x.key.urlsafe())
        soldier = soldier_key.get()
        soldier.badgeFreeFall = 0
        soldier.put()


def fix_unicode(data):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, dict):
        data = dict((fix_unicode(k), fix_unicode(data[k])) for k in data)
    elif isinstance(data, list):
        for i in xrange(0, len(data)):
            data[i] = fix_unicode(data[i])
    return data


def unicodestrip(uni):
    x = ast.literal_eval(uni)
    return x
