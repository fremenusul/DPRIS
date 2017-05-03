import webapp2
import jinja2
import os
import calendar
import ranks
import logging
import models
import datetime

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {

        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class SoldierPage(webapp2.RequestHandler):
    def get(self):
        s_query = models.SoldierData.query()
        soldier_data = s_query.fetch()

        template_values = {
            'soldiers': soldier_data,

        }

        template = jinja_environment.get_template('soldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        # TODO(Shangpo): Need to fix this to ensure each platoon can work.
        # TODO(Pull off into a different function to OOP this. Also add a dict to loop
        e = models.SoldierData(
            soldierName=self.request.get('name'),
            addedDate=datetime.datetime.now().date(),
            lastPromoted=datetime.datetime.now().date(),
            platoon=self.request.get('platoon'),
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
            medCombatHelo=0
        )
        e.put()

        return self.redirect('/soldier')


class DetailSoldier(webapp2.RequestHandler):
    def get(self):
        soldier_id = self.request.get('soldier')
        soldier_key = models.get_entity_from_url_safe_key(soldier_id)
        soldier_data = soldier_key
        nextRank = ranks.rankBuilder(soldier_data.rank)
        certs = []
        certs.append(soldier_data.certNCOPD1)
        certs.append(soldier_data.certNCOPD2)
        certs.append(soldier_data.certNCOPD3)
        certs.append(soldier_data.certAirAssult)
        certs.append(soldier_data.certSapper)
        certs.append(soldier_data.certRanger)
        certs.append(soldier_data.certPathfinder)
        certs.append(soldier_data.certFO)
        certs.append(soldier_data.certFDC)
        certs.append(soldier_data.certJFO)
        certs.append(soldier_data.certDMR)
        certs.append(soldier_data.certRSLC)
        certs.append(soldier_data.certRotor)
        certs.append(soldier_data.certRecruit)
        certstotal = sum(certs)
        ribbons = []
        ribbons.append(soldier_data.ribPistol)
        ribbons.append(soldier_data.ribStaff)
        ribbons.append(soldier_data.ribCommand)
        ribbons.append(soldier_data.ribAT)
        ribbons.append(soldier_data.ribGround)
        ribbons.append(soldier_data.ribDM)
        ribbons.append(soldier_data.ripSupport)
        ribbontotal = sum(ribbons)
        badges = []
        badges.append(soldier_data.badgeJump)
        badges.append(soldier_data.badgeCIB)
        badges.append(soldier_data.badgeIB)
        badges.append(soldier_data.badgeMedic)
        badges.append(soldier_data.badgeExplosive)
        badges.append(soldier_data.badgeCAB)
        badges.append(soldier_data.badgeAirDefense)
        badges.append(soldier_data.badgeArmor)
        badges.append(soldier_data.badgeTransport)
        badges.append(soldier_data.badgeCombatMedic)
        badgestotal = sum(badges)
        medals = []
        medals.append(soldier_data.medArmedForces)
        medals.append(soldier_data.medNationalDefense)
        medals.append(soldier_data.medDSM)
        medals.append(soldier_data.medMOV)
        medals.append(soldier_data.medCommendation)
        medals.append(soldier_data.medAchievement)
        medals.append(soldier_data.medDsync)
        medals.append(soldier_data.medConduct)
        medals.append(soldier_data.medPH)
        medals.append(soldier_data.medVolunteer)
        medals.append(soldier_data.medDSC)
        medals.append(soldier_data.medMerit)
        medals.append(soldier_data.medBronze)
        medals.append(soldier_data.medSilver)
        medals.append(soldier_data.medAir)
        medals.append(soldier_data.medAFCombatAction)
        medals.append(soldier_data.medCombatHelo)
        medalstotal = sum(medals)

        # logging.info(soldier_data)


        template_values = {
            'soldier': soldier_data,
            'soldier_id': soldier_id,
            'nextRank': nextRank,
            'certstotal': certstotal,
            'ribbontotal' : ribbontotal,
            'badgestotal' : badgestotal,
            'medalstotal' : medalstotal
        }

        template = jinja_environment.get_template('detailsoldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        if self.request.get('action') == 'certRifle':
            soldier_id = self.request.get('soldier')
            form = self.request.get('certRifle')
            models.update_rifle(soldier_id, form)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certNCOPD1':
            soldier_id = self.request.get('soldier')
            models.update_ncopd1(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certNCOPD2':
            soldier_id = self.request.get('soldier')
            models.update_ncopd2(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certNCOPD3':
            soldier_id = self.request.get('soldier')
            models.update_ncopd3(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certAirAssult':
            soldier_id = self.request.get('soldier')
            models.update_certAirAssult(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certSapper':
            soldier_id = self.request.get('soldier')
            models.update_certSapper(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certRanger':
            soldier_id = self.request.get('soldier')
            models.update_certRanger(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certPathfinder':
            soldier_id = self.request.get('soldier')
            models.update_certPathfinder(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certFO':
            soldier_id = self.request.get('soldier')
            models.update_certFO(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certFDC':
            soldier_id = self.request.get('soldier')
            models.update_certFDC(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certJFO':
            soldier_id = self.request.get('soldier')
            models.update_certJFO(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certDMR':
            soldier_id = self.request.get('soldier')
            models.update_certDMR(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certRSLC':
            soldier_id = self.request.get('soldier')
            models.update_certRSLC(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certRotor':
            soldier_id = self.request.get('soldier')
            models.update_certRotor(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'certRecruit':
            soldier_id = self.request.get('soldier')
            models.update_certRecruit(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribPistol':
            soldier_id = self.request.get('soldier')
            models.update_ribPistol(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribStaff':
            soldier_id = self.request.get('soldier')
            models.update_ribStaff(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribCommand':
            soldier_id = self.request.get('soldier')
            models.update_ribCommand(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribAT':
            soldier_id = self.request.get('soldier')
            models.update_ribAT(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribGround':
            soldier_id = self.request.get('soldier')
            models.update_ribGround(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ribDM':
            soldier_id = self.request.get('soldier')
            models.update_ribDM(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'ripSupport':
            soldier_id = self.request.get('soldier')
            models.update_ripSupport(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeJump':
            soldier_id = self.request.get('soldier')
            models.update_badgeJump(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeCIB':
            soldier_id = self.request.get('soldier')
            models.update_badgeCIB(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeIB':
            soldier_id = self.request.get('soldier')
            models.update_badgeIB(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeMedic':
            soldier_id = self.request.get('soldier')
            models.update_badgeMedic(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeExplosive':
            soldier_id = self.request.get('soldier')
            models.update_badgeExplosive(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeCAB':
            soldier_id = self.request.get('soldier')
            models.update_badgeCAB(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeAirDefense':
            soldier_id = self.request.get('soldier')
            models.update_badgeAirDefense(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeArmor':
            soldier_id = self.request.get('soldier')
            models.update_badgeArmor(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeTransport':
            soldier_id = self.request.get('soldier')
            models.update_badgeTransport(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'badgeCombatMedic':
            soldier_id = self.request.get('soldier')
            models.update_badgeCombatMedic(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medArmedForces':
            soldier_id = self.request.get('soldier')
            models.update_medArmedForces(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medNationalDefense':
            soldier_id = self.request.get('soldier')
            models.update_medNationalDefense(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medDSM':
            soldier_id = self.request.get('soldier')
            models.update_medDSM(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medMOV':
            soldier_id = self.request.get('soldier')
            models.update_medMOV(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medCommendation':
            soldier_id = self.request.get('soldier')
            models.update_medCommendation(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medAchievement':
            soldier_id = self.request.get('soldier')
            models.update_medAchievement(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medDsync':
            soldier_id = self.request.get('soldier')
            models.update_medDsync(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medConduct':
            soldier_id = self.request.get('soldier')
            models.update_medConduct(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medPH':
            soldier_id = self.request.get('soldier')
            models.update_medPH(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medVolunteer':
            soldier_id = self.request.get('soldier')
            models.update_medVolunteer(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medDSC':
            soldier_id = self.request.get('soldier')
            models.update_medDSC(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medMerit':
            soldier_id = self.request.get('soldier')
            models.update_medMerit(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medBronze':
            soldier_id = self.request.get('soldier')
            models.update_medBronze(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medSilver':
            soldier_id = self.request.get('soldier')
            models.update_medSilver(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medAir':
            soldier_id = self.request.get('soldier')
            models.update_medAir(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medAFCombatAction':
            soldier_id = self.request.get('soldier')
            models.update_medAFCombatAction(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medCombatHelo':
            soldier_id = self.request.get('soldier')
            models.update_medCombatHelo(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'promotepv2':
            soldier_id = self.request.get('soldier')
            models.update_soldier_from_rct(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'promote':
            soldier_id = self.request.get('soldier')
            nextRank = self.request.get('rank')
            models.promote_soldier(soldier_id, nextRank)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)


class Attendance(webapp2.RequestHandler):
    def get(self):
        cal = calendar.Calendar()
        # TODO(Shangpo): Make auto month
        monthdates = [x for x in cal.itermonthdays(2017, 5) if x != 0]
        s_query = models.SoldierData.query()
        soldier_data = s_query.fetch()

        # logging.info(monthdates)

        template_values = {
            'monthdays': monthdates,
            'soldiers': soldier_data,
        }

        template = jinja_environment.get_template('attendance.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
    ('/detailsoldier', DetailSoldier),
    ('/attendance', Attendance),
], debug=True)
