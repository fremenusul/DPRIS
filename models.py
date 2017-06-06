import datetime

from google.appengine.ext import ndb

import tz2ntz


class SoldierData(ndb.Model):
    addedDate = ndb.DateProperty(indexed=False)
    soldierName = ndb.StringProperty()
    platoon = ndb.StringProperty()
    rank = ndb.StringProperty()
    rankorder = ndb.IntegerProperty()
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
    certWings = ndb.IntegerProperty(indexed=False)
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
    badgeExplosive = ndb.IntegerProperty(indexed=False)
    badgeCAB = ndb.IntegerProperty(indexed=False)
    badgeAirDefense = ndb.IntegerProperty(indexed=False)
    badgeArmor = ndb.IntegerProperty(indexed=False)
    badgeTransport = ndb.IntegerProperty(indexed=False)
    badgeCombatMedic = ndb.IntegerProperty(indexed=False)
    badgeFreeFall = ndb.IntegerProperty(indexed=False)
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
    medAFCombatAction = ndb.IntegerProperty(indexed=False)
    medCombatHelo = ndb.IntegerProperty(indexed=False)
    medDFC = ndb.IntegerProperty(indexed=False)
    lastPromoted = ndb.DateProperty(indexed=False)
    num_certs = ndb.IntegerProperty()
    num_ribbons = ndb.IntegerProperty()
    num_badges = ndb.IntegerProperty()
    num_medals = ndb.IntegerProperty()
    num_awards = ndb.IntegerProperty()


class Attendance(ndb.Model):
    soldier_key = ndb.StringProperty()
    attendValue = ndb.StringProperty(indexed=False)
    attendDate = ndb.DateProperty()

class AttendanceChecker(ndb.Model):
    datecheck = ndb.DateProperty()
    platoon = ndb.StringProperty()
    attend = ndb.IntegerProperty()

def update_attendance(url_string, attendvalue):
    e = Attendance(
        soldier_key=url_string,
        attendDate=tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific'),
        attendValue=attendvalue
    )
    e.put()


def add_attendance(url_string, attendvalue, attenddate):
    e = Attendance(
        soldier_key=url_string,
        attendDate=attenddate,
        attendValue=attendvalue
    )
    e.put()

def delete_attendance(url_string):
    attend_key = ndb.Key(urlsafe=url_string)
    attend_key.delete()


def attendance_check(theplatoon):
    e = AttendanceChecker(
        platoon=theplatoon,
        datecheck=tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific'),
        attend= 1
    )
    e.put()


def get_entity_from_url_safe_key(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    return soldier


def update_soldier_from_rct(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.rank = "PV2"
    soldier.rankorder = 2
    soldier.badgeJump = 1
    soldier.num_badges += 1
    soldier.medArmedForces = 1
    soldier.num_medals += 1
    soldier.lastPromoted = tz2ntz.tz2ntz(datetime.datetime.today(), 'UTC', 'US/Pacific')
    soldier.put()

def change_attendance(url_string, attenddate, attendvalue, soldier_key):
    attend_key = ndb.Key(urlsafe=url_string)
    attend = attend_key.get()
    attend.attendDate = attenddate
    attend.attendValue = attendvalue
    attend.soldier_key = soldier_key
    attend.put()


def delete_soldier(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier_key.delete()


def update_soldier(url_string, name, joined, platoon, lastpromoted):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.soldierName = name
    soldier.addedDate = joined
    soldier.platoon = platoon
    soldier.lastPromoted = lastpromoted
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


def update_rifle(url_string, cert):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certRifle = cert
    soldier.num_certs += 1
    soldier.put()


def update_ncopd1(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certNCOPD1 = 1
    soldier.num_certs += 1
    soldier.put()


def update_ncopd2(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certNCOPD2 = 1
    soldier.num_certs += 1
    soldier.put()


def update_ncopd3(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certNCOPD3 = 1
    soldier.num_certs += 1
    soldier.put()


def update_certAirAssult(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certAirAssult = 1
    soldier.num_certs += 1
    soldier.put()


def update_certSapper(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certSapper = 1
    soldier.num_certs += 1
    soldier.put()


def update_certRanger(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certRanger = 1
    soldier.num_certs += 1
    soldier.put()


def update_certPathfinder(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certPathfinder = 1
    soldier.num_certs += 1
    soldier.put()


def update_certFO(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certFO = 1
    soldier.num_certs += 1
    soldier.put()


def update_certFDC(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certFDC = 1
    soldier.num_certs += 1
    soldier.put()


def update_certJFO(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certJFO = 1
    soldier.num_certs += 1
    soldier.put()


def update_certDMR(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certDMR = 1
    soldier.num_certs += 1
    soldier.put()


def update_certRSLC(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certRSLC = 1
    soldier.num_certs += 1
    soldier.put()


def update_certRecruit(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certRecruit = 1
    soldier.num_certs += 1
    soldier.put()


def update_ribPistol(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribPistol = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ribStaff(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribStaff = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ribCommand(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribCommand = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ribAT(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribAT = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ribGround(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribGround = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ribDM(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ribDM = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_ripSupport(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.ripSupport = 1
    soldier.num_ribbons += 1
    soldier.put()


def update_badgeJump(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeJump = 1
    soldier.put()


def update_badgeCIB(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeCIB = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeIB(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeIB = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeMedic(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeMedic = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeExplosive(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeExplosive = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeCAB(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeCAB = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeAirDefense(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeAirDefense = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeArmor(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeArmor = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeTransport(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeTransport = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeCombatMedic(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeCombatMedic = 1
    soldier.num_badges += 1
    soldier.put()


def update_badgeFreeFall(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.badgeFreeFall = 1
    soldier.num_badges += 1
    soldier.put()


def update_medArmedForces(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medArmedForces = 1
    soldier.num_medals += 1
    soldier.put()


def update_medNationalDefense(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medNationalDefense = 1
    soldier.num_medals += 1
    soldier.put()


def update_medDSM(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medDSM = 1
    soldier.num_medals += 1
    soldier.put()


def update_medMOV(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medMOV = 1
    soldier.num_medals += 1
    soldier.put()


def update_medCommendation(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medCommendation = 1
    soldier.num_medals += 1
    soldier.put()


def update_medAchievement(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medAchievement = 1
    soldier.num_medals += 1
    soldier.put()


def update_medDsync(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medDsync = 1
    soldier.put()


def update_medConduct(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medConduct = 1
    soldier.num_medals += 1
    soldier.put()


def update_medPH(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medPH = 1
    soldier.num_medals += 1
    soldier.put()


def update_medVolunteer(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medVolunteer = 1
    soldier.num_medals += 1
    soldier.put()


def update_medDSC(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medDSC = 1
    soldier.num_medals += 1
    soldier.put()


def update_medMerit(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medMerit = 1
    soldier.num_medals += 1
    soldier.put()


def update_medBronze(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medBronze = 1
    soldier.num_medals += 1
    soldier.put()


def update_medSilver(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medSilver = 1
    soldier.num_medals += 1
    soldier.put()

def update_certRotor(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certRotor = 1
    soldier.num_awards += 1
    soldier.put()


def update_certWings(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.certWings = 1
    soldier.num_awards += 1
    soldier.put()


def update_medAir(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medAir = 1
    soldier.num_awards += 1
    soldier.put()


def update_medAFCombatAction(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medAFCombatAction = 1
    soldier.num_awards += 1
    soldier.put()


def update_medCombatHelo(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medCombatHelo = 1
    soldier.num_awards += 1
    soldier.put()


def update_medDFC(url_string):
    soldier_key = ndb.Key(urlsafe=url_string)
    soldier = soldier_key.get()
    soldier.medDFC = 1
    soldier.num_awards += 1
    soldier.put()
