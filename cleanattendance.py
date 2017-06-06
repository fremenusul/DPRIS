import logging

import models


def cleaner():
    s_query = models.SoldierData.query()
    soldier_data = s_query.fetch()

    for x in soldier_data:
        a_query = models.Attendance.query(models.Attendance.soldier_key == x.key.urlsafe())
        attendance_data = a_query.fetch()
        # logging.info(attendance_data)
        # logging.info(len(attendance_data))
        for y in attendance_data:
            if y.soldier_key != x.key.urlsafe():
                logging.info('Key is broken ' + y.soldier_key)
                logging.info(x.soldierName + str(y.attendDate))
                # models.delete_soldier(y.key.urlsafe())
