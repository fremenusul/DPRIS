import calendar
import cgi
import datetime
import logging
import os

import jinja2
import webapp2
from google.appengine.api import memcache
from google.appengine.api import users

import checker
import models
import newsoldier
import ranks
import snippets
import tz2ntz

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        #Find current user
        user = users.get_current_user()
        #If user exists, show logout and get user email
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user_email = user.email()
        #If user does not exist, create login and create a default to ensure checks work.
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            user_email = 'none@none.com'

        template_values = {
            'user': user,
            'user_email': user_email,
            'url': url,
            'url_linktext': url_linktext
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class SoldierPage(webapp2.RequestHandler):
    def get(self):
        platoon = self.request.get('platoon')
        user = users.get_current_user()
        #Get user email and check to see if the person is authorized to make changes in checker.py
        if user:
            user_email = user.email()
            auth = checker.isIC(user_email)
        else:
            auth = False, 'N/A'
        if auth[0] is True:
            auth_ic = True
        else:
            auth_ic = False
        #If RCT pull direct, no memecache
        if platoon == 'none':
            s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
                -models.SoldierData.rankorder, models.SoldierData.soldierName)
            soldier_data = s_query.fetch()
        else:
            results = memcache.get(platoon)
            soldier_data = results
            if not results:
                s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
                    -models.SoldierData.rankorder, models.SoldierData.soldierName)
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
        #check to see if someone added nothing, return to page.
        soldiername = self.request.get('name')
        if soldiername == "":
            return self.redirect('/soldier?platoon=none')
        #cgi escape to ensure no bad things. Add soldier.
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

        template_values = {
            'soldier': soldier_data,
            'soldier_id': soldier_id,
            'nextRank': nextRank,
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
        elif self.request.get('action') == 'badgeFreeFall':
            soldier_id = self.request.get('soldier')
            models.update_badgeFreeFall(soldier_id)
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
            lastpromote = self.request.get('lastpromote')
            joined_date = datetime.datetime.strptime(joined, '%Y-%m-%d')
            promote_date = datetime.datetime.strptime(lastpromote, '%Y-%m-%d')
            models.update_soldier(soldier_id, cgi.escape(soldiername), joined_date, platoon, promote_date)
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
        #Build Cal object
        cal = calendar.Calendar()
        #date object
        current_month = datetime.datetime.today()
        #get current month by name
        long_month = current_month.strftime("%B")
        #build the number of days in a month
        monthdates = [x for x in cal.itermonthdays(current_month.year, current_month.month) if x != 0]
        #get current day fixed
        today = tz2ntz.tz2ntz(current_month, 'UTC', 'US/Pacific')
        #Print today
        todaydate = datetime.datetime.strftime(today, '%B %d')
        #Fetch soldier data
        s_query = models.SoldierData.query(models.SoldierData.platoon == platoon).order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        # TODO(Shangpo) Add filter to grab this current month only. Investigate why filters don't work
        holder = []
        # first_day = snippets.get_first_day(current_month)
        # startdate = datetime.date(first_day)
        startdate = snippets.get_first_day(today)
        for x in soldier_data:
            a_query = models.Attendance.query(models.Attendance.soldier_key == x.key.urlsafe())
            # a_query = a_query.filter(models.Attendance.attendDate >= startdate)
            # thekey = x.key.urlsafe()
            # a_query = ndb.gql("SELECT * FROM Attendance WHERE soldier_key = '%s' AND attendDate > DATE('2017-05-01')" % thekey)
            attendance_data = a_query.fetch()

            p = []
            a = []
            t = []
            dev = []
            datelist = []
            for y in attendance_data:
                if y.attendDate < startdate:
                    continue
                day_num = int(datetime.datetime.strftime(y.attendDate, '%d'))
                value = y.attendValue
                if value == 'T':
                    t.append(1)
                elif value == 'HP':
                    t.append(0.5)
                    p.append(1)
                elif value == 'H':
                    t.append(0.5)
                elif value == '/':
                    dev.append(1)
                elif value =='A':
                    a.append(1)
                elif value =='P':
                    p.append(1)
                datelist.append((day_num, value))
            present = sum(p)
            absent = sum(a)
            training = sum(t)
            holder.append((x, datelist, present, absent, training))

        attend_query = models.AttendanceChecker.query(
            models.AttendanceChecker.platoon == platoon and models.AttendanceChecker.datecheck == today)
        attend_data = attend_query.fetch()

        if len(attend_data) > 0:
            platoon_attendance = True
        else:
            platoon_attendance = False

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
            'auth_platoon': auth_platoon,
            'attendance_data': holder,
            'platoon_attendance' : platoon_attendance
        }

        template = jinja_environment.get_template('attendance.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        platoon = self.request.get('platoon')
        values = []
        for field in self.request.get_all('attendance'):
            values.append(field)

        soldiers = []
        for field in self.request.get_all('soldier_id'):
            soldiers.append(field)

        num_entities = len(values) - 1

        x = 0
        while x <= num_entities:
            models.update_attendance(soldiers[x].encode('utf-8'), values[x])
            x += 1
        models.attendance_check(platoon)
        return self.redirect('/attendance?platoon=' + platoon)




# REMOVE BEFORE LIVE
class UpdateModel(webapp2.RequestHandler):
    def get(self):
        snippets.updatemodel3()

        template_values = {

        }

        return self.redirect('/soldier?platoon=none')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
    ('/detailsoldier', DetailSoldier),
    ('/attendance', Attendance),
    ('/model', UpdateModel),
], debug=True)
