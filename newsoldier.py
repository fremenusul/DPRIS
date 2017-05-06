import models
import datetime


def addnewsoldier(soldiername):
    e = models.SoldierData(
        soldierName=soldiername,
        addedDate=datetime.datetime.now().date(),
        lastPromoted=datetime.datetime.now().date(),
        platoon='none',
        rank='RCT',
        certRifle='None',
        certNCOPD1=0,
        certNCOPD2=0,
        certNCOPD3=0,
        certAirAssult=0,
        certSapper=0,
        certRanger=0,
        certPathfinder=0,
        certFO=0,
        certFDC=0,
        certJFO=0,
        certDMR=0,
        certRSLC=0,
        certRotor=0,
        certWings=0,
        certRecruit=0,
        ribPistol=0,
        ribStaff=0,
        ribCommand=0,
        ribAT=0,
        ribGround=0,
        ribDM=0,
        ripSupport=0,
        badgeJump=0,
        badgeCIB=0,
        badgeIB=0,
        badgeMedic=0,
        badgeExplosive=0,
        badgeCAB=0,
        badgeAirDefense=0,
        badgeArmor=0,
        badgeTransport=0,
        badgeCombatMedic=0,
        medArmedForces=0,
        medNationalDefense=0,
        medDSM=0,
        medMOV=0,
        medCommendation=0,
        medAchievement=0,
        medDsync=0,
        medConduct=0,
        medPH=0,
        medVolunteer=0,
        medDSC=0,
        medMerit=0,
        medBronze=0,
        medSilver=0,
        medAir=0,
        medAFCombatAction=0,
        medCombatHelo=0,
        medDFC=0
    )
    e.put()
