import calendar
import cgi
import datetime
import logging
import os
import urllib

import jinja2
import webapp2

import models
import ranks
import newsoldier
import checker
import tz2ntz

from google.appengine.api import memcache
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info(user)
        
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user_email = user.email()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            user_email = 'none@none.com'
        template_values = {
            'user': user,
            'user_email' : user_email,
            'url': url,
            'url_linktext': url_linktext
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class SoldierPage(webapp2.RequestHandler):
    def get(self):
        platoon = self.request.get('platoon')
        user = users.get_current_user()
        if user:
            user_email = user.email()
            auth = checker.isIC(user_email)
        else:
            auth = False, 'N/A'
        if auth[0] is True:
            auth_ic = True
        else:
            auth_ic = False
        if platoon == 'none':
            s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
                -models.SoldierData.rankorder)
            soldier_data = s_query.fetch()
        else:
            results = memcache.get(platoon)
            soldier_data = results
            if not results:
                s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
                -models.SoldierData.rankorder)
                soldier_data = s_query.fetch()
                memcache.set(platoon, soldier_data, 30)
                logging.info('No Cache')

        template_values = {
            'soldiers': soldier_data,
            'platoon': platoon,
            'auth_ic': auth_ic,

        }

        template = jinja_environment.get_template('soldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        soldiername = self.request.get('name')
        if soldiername == "":
            return self.redirect('/soldier?platoon=none')
        else:
            newsoldier.addnewsoldier(cgi.escape(soldiername))
            return self.redirect('/soldier?platoon=none')


class DetailSoldier(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
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
        soldier_id = self.request.get('soldier')
        soldier_key = models.get_entity_from_url_safe_key(soldier_id)
        soldier_data = soldier_key
        nextRank = ranks.rankBuilder(soldier_data.rank)

        certs = []
        if soldier_data.certRifle != 'None':
            certs.append(1)
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
        medalstotal = sum(medals)

        av = []
        av.append(soldier_data.certRotor)
        av.append(soldier_data.certWings)
        av.append(soldier_data.medAir)
        av.append(soldier_data.medAFCombatAction)
        av.append(soldier_data.medCombatHelo)
        av.append(soldier_data.medDFC)
        avtotal = sum(av)

        template_values = {
            'soldier': soldier_data,
            'soldier_id': soldier_id,
            'nextRank': nextRank,
            'certstotal': certstotal,
            'ribbontotal': ribbontotal,
            'badgestotal': badgestotal,
            'medalstotal': medalstotal,
            'avtotal': avtotal,
            'auth_ic': auth_ic,
            'auth_platoon': auth_platoon

        }

        template = jinja_environment.get_template('detailsoldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        if self.request.get('action') == 'certRifle':
            soldier_id = self.request.get('soldier')
            rifle = self.request.get('certRifle')
            models.update_rifle(soldier_id, rifle)
            logging.info(rifle)
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
        elif self.request.get('action') == 'certWings':
            soldier_id = self.request.get('soldier')
            models.update_certWings(soldier_id)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'medDFC':
            soldier_id = self.request.get('soldier')
            models.update_medDFC(soldier_id)
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
        elif self.request.get('action') == 'editsoldier':
            soldier_id = self.request.get('soldier')
            soldiername = self.request.get('name')
            joined = self.request.get('joined')
            platoon = self.request.get('platoon')
            joined_date = datetime.datetime.strptime(joined, '%Y-%m-%d')
            models.update_soldier(soldier_id, cgi.escape(soldiername), joined_date, platoon)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'deletesoldier':
            soldier_id = self.request.get('soldier')
            platoon = self.request.get('platoon')
            models.delete_soldier(soldier_id)
            return self.redirect('/soldier?platoon=' + platoon)


class Attendance(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        platoon = self.request.get('platoon')
        cal = calendar.Calendar()
        current_month = datetime.datetime.today()
        long_month = current_month.strftime("%B")
        monthdates = [x for x in cal.itermonthdays(current_month.year, current_month.month) if x != 0]
        today = tz2ntz.tz2ntz(current_month, 'UTC', 'US/Pacific')
        todaydate = datetime.datetime.strftime(today, '%B %d')
        s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
                -models.SoldierData.rankorder)
        soldier_data = s_query.fetch()

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

        template_values = {
            'todaydate': todaydate,
            'soldiers': soldier_data,
            'monthname': long_month,
            'platoon': platoon,
            'monthdays': monthdates,
            'auth_ic': auth_ic,
            'auth_platoon': auth_platoon
        }

        template = jinja_environment.get_template('attendance.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        values = []
        for field in self.request.get_all('attendance'):
            values.append(field)

        soldiers = []
        for field in self.request.get_all('soldier_id'):
            soldiers.append(field)

        num_entities = len(values) -1

        x = 0
        while x <= num_entities:
            models.update_attendance(soldiers[x], values[x])
            x +=1






# REMOVE BEFORE LIVE
class TestSoldier(webapp2.RequestHandler):
    def get(self):
        testsoldiers = ['Frank', 'Mike', 'Jessie', 'Sam', 'Cranky', 'Noveske', 'Ringo', 'Boltz', 'Larry', 'Albert',
                        'Lanky Pete', 'Keyser Soze', 'Poopy McPooperson', 'Joe Schmuckatelli']

        for i in testsoldiers:
            newsoldier.addnewsoldier(i)

        template_values = {

        }

        return self.redirect('/soldier?platoon=none')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
    ('/detailsoldier', DetailSoldier),
    ('/attendance', Attendance),
    ('/test', TestSoldier),
], debug=True)
