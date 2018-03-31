import datetime

from google.appengine.ext import ndb

import tz2ntz


class SoldierData(ndb.Model):
    addedDate = ndb.DateProperty(indexed=False)
    soldierName = ndb.StringProperty()
    platoon = ndb.StringProperty()
    rank = ndb.StringProperty()
    xmlid = ndb.IntegerProperty()
    rankorder = ndb.IntegerProperty()
    lastPromoted = ndb.DateProperty(indexed=False)


def get_entity_from_url_safe_key(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    return soldier


def update_soldier_from_rct(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.rank = "PV2"
    soldier.rankorder = 2
    soldier.lastPromoted = tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific')
    soldier.put()

def delete_soldier(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier_key.delete()


def update_soldier(url_string, name, joined, platoon, lastpromoted, xmlid):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.soldierName = name
    soldier.addedDate = joined
    soldier.platoon = platoon
    soldier.lastPromoted = lastpromoted
    soldier.xmlid = xmlid
    soldier.put()


def update_platoon(url_string, platoon):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.platoon = platoon


def promote_soldier(url_string, rank):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.rank = rank
    soldier.rankorder += 1
    soldier.lastPromoted = tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific')
    soldier.put()


def demote_soldier(url_string, rank):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.rank = rank
    soldier.rankorder -= 1
    soldier.lastPromoted = tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific')
    soldier.put()


def updateXMLID(url_string, xmlid):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.xmlid = xmlid
    soldier.put()

