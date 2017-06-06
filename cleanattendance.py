import logging

import models


def cleaner():
    s_query = models.SoldierData.query()
    soldier_data = s_query.fetch(keys_only=True)

    soldierid = []

    for x in soldier_data:
        soldierid.append(x.urlsafe())

    a_query = models.Attendance.query()
    attendance_data = a_query.fetch()
    thelist = []
    for y in attendance_data:
        if y.soldier_key not in soldierid:
            thelist.append(y.soldier_key)
    return list(set(thelist))
