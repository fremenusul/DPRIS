import datetime

import models
import tz2ntz


def addnewsoldier(soldiername):
    e = models.SoldierData(
        soldierName=soldiername,
        addedDate=tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific'),
        lastPromoted=tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific'),
        platoon='none',
        rank='RCT',
        xmlid=0,
        rankorder=1,
    )
    e.put()