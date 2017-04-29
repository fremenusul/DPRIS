from google.appengine.ext import ndb


class SoldierData(ndb.Model):
    addedDate = ndb.DateProperty(indexed=False)
    soldierName = ndb.StringProperty(indexed=False)
    platoon = ndb.StringProperty(indexed=False)
    rank = ndb.StringProperty(indexed=False)
    certRifle = ndb.StringProperty(indexed=False)
    certNCOPD1 = ndb.IntegerProperty(indexed=False)
    certNCOPD2 = ndb.IntegerProperty(indexed=False)
    certNCOPD3 = ndb.IntegerProperty(indexed=False)
    certAirAssult = ndb.IntegerProperty(indexed=False)
    certSapper = ndb.IntegerProperty(indexed=False)
    certRanger = ndb.IntegerProperty(indexed=False)
    certPathfinder = ndb.IntegerProperty(indexed=False)
    certFO = ndb.IntegerProperty(indexed=False)
    certFDC = ndb.IntegerProperty(indexed=False)
    certJFO = ndb.IntegerProperty(indexed=False)
    certDMR = ndb.IntegerProperty(indexed=False)
    certRSLC = ndb.IntegerProperty(indexed=False)
    certRotor = ndb.IntegerProperty(indexed=False)
    certRecruit = ndb.IntegerProperty(indexed=False)
    ribPistol = ndb.IntegerProperty(indexed=False)
    ribStaff = ndb.IntegerProperty(indexed=False)
    ribCommand = ndb.IntegerProperty(indexed=False)
    ribAT = ndb.IntegerProperty(indexed=False)
    ribGround = ndb.IntegerProperty(indexed=False)
    ribDM = ndb.IntegerProperty(indexed=False)
    ripSupport = ndb.IntegerProperty(indexed=False)
    badgeJump = ndb.IntegerProperty(indexed=False)
    badgeCIB = ndb.IntegerProperty(indexed=False)
    badgeIB = ndb.IntegerProperty(indexed=False)
    badgeMedic = ndb.IntegerProperty(indexed=False)
    badgeExposive = ndb.IntegerProperty(indexed=False)
    badgeCAB = ndb.IntegerProperty(indexed=False)
    badgeAirDefense = ndb.IntegerProperty(indexed=False)
    badgeArmor = ndb.IntegerProperty(indexed=False)
    badgeTransport = ndb.IntegerProperty(indexed=False)
    badgeCombatMedic = ndb.IntegerProperty(indexed=False)
    medArmedForces = ndb.IntegerProperty(indexed=False)
    medNationalDefense = ndb.IntegerProperty(indexed=False)
    medDSM = ndb.IntegerProperty(indexed=False)
    medMOV = ndb.IntegerProperty(indexed=False)
    medCommendation = ndb.IntegerProperty(indexed=False)
    medAchievement = ndb.IntegerProperty(indexed=False)
    medDsync = ndb.IntegerProperty(indexed=False)
    medConduct = ndb.IntegerProperty(indexed=False)
    medPH = ndb.IntegerProperty(indexed=False)
    medVolunteer = ndb.IntegerProperty(indexed=False)
    medDSC = ndb.IntegerProperty(indexed=False)
    medMerit = ndb.IntegerProperty(indexed=False)
    medBronze = ndb.IntegerProperty(indexed=False)
    medSilver = ndb.IntegerProperty(indexed=False)
    medAir = ndb.IntegerProperty(indexed=False)
    medAFCombatAction= ndb.IntegerProperty(indexed=False)
    medCombatHelo = ndb.IntegerProperty(indexed=False)
    lastPromoted = ndb.DateProperty(indexed=False)

def get_entity_from_url_safe_key(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    return soldier








