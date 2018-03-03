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
        # Find current user
        user = users.get_current_user()
        # If user exists, show logout and get user email
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user_email = user.email()
        # If user does not exist, create login and create a default to ensure checks work.
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
        # Get user email and check to see if the person is authorized to make changes in checker.py
        if user:
            user_email = user.email()
            auth = checker.isIC(user_email)
        else:
            auth = False, 'N/A'
        if auth[0] is True:
            auth_ic = True
        else:
            auth_ic = False
        # If RCT pull direct, no memecache
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

        template_values = {
            'soldiers': soldier_data,
            'platoon': platoon,
            'auth_ic': auth_ic,

        }

        template = jinja_environment.get_template('soldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        # check to see if someone added nothing, return to page.
        soldiername = self.request.get('name')
        platoon = self.request.get('platoon')
        if soldiername == "":
            return self.redirect('/soldier?platoon=none')
        # cgi escape to ensure no bad things. Add soldier.
        else:
            newsoldier.addnewsoldier(cgi.escape(soldiername))
            memcache.delete(platoon, 0)
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
        if soldier_data.platoon == 'whiskey':
            nextRank = ranks.rankBuilderW(soldier_data.rank)
        else:
            nextRank = ranks.rankBuilder(soldier_data.rank)
        demote = ranks.rankDemote(soldier_data.rank)

        template_values = {
            'soldier': soldier_data,
            'soldier_id': soldier_id,
            'nextRank': nextRank,
            'auth_ic': auth_ic,
            'auth_platoon': auth_platoon,
            #'monthdays': monthdates,
            'prevRank': demote,

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
            platoon = self.request.get('platoon')
            nextRank = self.request.get('rank')
            models.promote_soldier(soldier_id, nextRank)
            memcache.delete(platoon)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'demote':
            soldier_id = self.request.get('soldier')
            platoon = self.request.get('platoon')
            prevRank = self.request.get('rank')
            models.demote_soldier(soldier_id, prevRank)
            memcache.delete(platoon)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'editsoldier':
            soldier_id = self.request.get('soldier')
            soldiername = self.request.get('name')
            joined = self.request.get('joined')
            platoon = self.request.get('platoon')
            lastpromote = self.request.get('lastpromote')
            xmlidform = self.request.get('xmlid')
            xmlid = long(xmlidform)
            joined_date = datetime.datetime.strptime(joined, '%Y-%m-%d')
            promote_date = datetime.datetime.strptime(lastpromote, '%Y-%m-%d')
            models.update_soldier(soldier_id, cgi.escape(soldiername), joined_date, platoon, promote_date, xmlid)
            memcache.delete(platoon, 0)
            return self.redirect('/detailsoldier?soldier=' + soldier_id)
        elif self.request.get('action') == 'deletesoldier':
            soldier_id = self.request.get('soldier')
            platoon = self.request.get('platoon')
            models.delete_soldier(soldier_id)
            memcache.delete(platoon, 0)
            return self.redirect('/soldier?platoon=' + platoon)
        elif self.request.get('action') == 'editattendance':
            platoon = self.request.get('platoon')
            attend_keys = snippets.fix_unicode(self.request.get_all('key'))
            # logging.info(attend_keys)
            values = snippets.fix_unicode(self.request.get_all('value'))
            # logging.info(values)
            datevalue = snippets.fix_unicode(self.request.get_all('date'))
            # logging.info(len(datevalue))
            soldier_id = self.request.get('soldier')
            z = 0
            for x in datevalue:
                # logging.info(z)
                attend_key = attend_keys[z]
                # logging.info('Attend key' + attend_key)
                fixeddate = datetime.datetime.strptime(datevalue[z], '%Y-%m-%d')
                # logging.info('Date' + str(fixeddate))
                fieldname = values[z]
                # logging.info('Value' +fieldname)
                z += 1
                models.change_attendance(attend_key, fixeddate, fieldname, soldier_id)
            # TODO(Shangpo) Run a checker here to handle any changes to totals.

            return self.redirect('/detailsoldier?soldier=' + soldier_id)





# REMOVE BEFORE LIVE
class UpdateModel(webapp2.RequestHandler):
    def get(self):
        #snippets.updatemodel4()
        #cleanattendance.cleaner()

        template_values = {

        }

        # return self.redirect('/soldier?platoon=none')





class VikingXML(webapp2.RequestHandler):
    def get(self):

        s_query = models.SoldierData.query(models.SoldierData.platoon == 'viking').order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        self.response.headers['Content-Type'] = "application/xml"
        headerxml = """<?xml version="1.0"?>
        <!DOCTYPE squad SYSTEM "squad.dtd">
        <?xml-stylesheet href="squad.xsl" type="text/xsl"?>
        <squad nick="2nd">
        <name>2nd Platoon "Viking"</name>
        <email>N/A</email>
        <web>http://21starmyrangers.enjin.com/</web>
        <picture>21stLogo_VikingPatch.paa</picture>
        <title>2nd Platoon "Viking"</title> \n"""
        self.response.write(headerxml)
        for x in soldier_data:
            primexml = '<member id="' + str(x.xmlid) + '" nick="' + x.rank + ' ' + x.soldierName + '"><name>' + x.rank + ' ' + x.soldierName +' </name><email>N/A</email><icq>N/A</icq><remark>N/A</remark></member> \n'
            self.response.write(primexml)
        bottomxml = '</squad>'
        self.response.write(bottomxml)

class NightmareXML(webapp2.RequestHandler):
    def get(self):

        s_query = models.SoldierData.query(models.SoldierData.platoon == 'nightmare').order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        self.response.headers['Content-Type'] = "application/xml"
        headerxml = """<?xml version="1.0"?>
        <!DOCTYPE squad SYSTEM "squad.dtd">
        <?xml-stylesheet href="squad.xsl" type="text/xsl"?>
        <squad nick="1st">
        <name>1st Platoon "Nightmare"</name>
        <email>N/A</email>
        <web>http://21starmyrangers.enjin.com/</web>
        <picture>21stLogo_NightmarePatch.paa</picture>
        <title>1st Platoon "Nightmare"</title> \n"""
        self.response.write(headerxml)
        for x in soldier_data:
            primexml = '<member id="' + str(x.xmlid) + '" nick="' + x.rank + ' ' + x.soldierName + '"><name>' + x.rank + ' ' + x.soldierName +' </name><email>N/A</email><icq>N/A</icq><remark>N/A</remark></member> \n'
            self.response.write(primexml)
        bottomxml = '</squad>'
        self.response.write(bottomxml)

class GuardianXML(webapp2.RequestHandler):
    def get(self):

        s_query = models.SoldierData.query(models.SoldierData.platoon == 'guardian').order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        self.response.headers['Content-Type'] = "application/xml"
        headerxml = """<?xml version="1.0"?>
        <!DOCTYPE squad SYSTEM "squad.dtd">
        <?xml-stylesheet href="squad.xsl" type="text/xsl"?>
        <squad nick="3rd">
        <name>3rd Platoon "Guardian"</name>
        <email>N/A</email>
        <web>http://21starmyrangers.enjin.com/</web>
        <picture>21stLogo_GuardianPatch.paa</picture>
        <title>3rd Platoon "Guardian"</title> \n"""
        self.response.write(headerxml)
        for x in soldier_data:
            primexml = '<member id="' + str(x.xmlid) + '" nick="' + x.rank + ' ' + x.soldierName + '"><name>' + x.rank + ' ' + x.soldierName +' </name><email>N/A</email><icq>N/A</icq><remark>N/A</remark></member> \n'
            self.response.write(primexml)
        bottomxml = '</squad>'
        self.response.write(bottomxml)

class WhiskeyXML(webapp2.RequestHandler):
    def get(self):

        s_query = models.SoldierData.query(models.SoldierData.platoon == 'whiskey').order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        self.response.headers['Content-Type'] = "application/xml"
        headerxml = """<?xml version="1.0"?>
        <!DOCTYPE squad SYSTEM "squad.dtd">
        <?xml-stylesheet href="squad.xsl" type="text/xsl"?>
        <squad nick="Whiskey">
        <name>Whiskey</name>
        <email>N/A</email>
        <web>http://21starmyrangers.enjin.com/</web>
        <picture>21stLogo_WhiskeyPatch.paa</picture>
        <title>Whiskey</title> \n"""
        self.response.write(headerxml)
        for x in soldier_data:
            primexml = '<member id="' + str(x.xmlid) + '" nick="' + x.rank + ' ' + x.soldierName + '"><name>' + x.rank + ' ' + x.soldierName +' </name><email>N/A</email><icq>N/A</icq><remark>N/A</remark></member> \n'
            self.response.write(primexml)
        bottomxml = '</squad>'
        self.response.write(bottomxml)

class TOCXML(webapp2.RequestHandler):
    def get(self):

        s_query = models.SoldierData.query(models.SoldierData.platoon == 'toc').order(
            -models.SoldierData.rankorder, models.SoldierData.soldierName)
        soldier_data = s_query.fetch()

        self.response.headers['Content-Type'] = "application/xml"
        headerxml = """<?xml version="1.0"?>
        <!DOCTYPE squad SYSTEM "squad.dtd">
        <?xml-stylesheet href="squad.xsl" type="text/xsl"?>
        <squad nick="TOC">
        <name>TOC</name>
        <email>N/A</email>
        <web>http://21starmyrangers.enjin.com/</web>
        <picture>21stLogo_TOCPatch.paa</picture>
        <title>TOC</title> \n"""
        self.response.write(headerxml)
        for x in soldier_data:
            primexml = '<member id="' + str(x.xmlid) + '" nick="' + x.rank + ' ' + x.soldierName + '"><name>' + x.rank + ' ' + x.soldierName +' </name><email>N/A</email><icq>N/A</icq><remark>N/A</remark></member> \n'
            self.response.write(primexml)
        bottomxml = '</squad>'
        self.response.write(bottomxml)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
    ('/detailsoldier', DetailSoldier),
    ('/model', UpdateModel),
    ('/viking/squad.xml', VikingXML),
    ('/nightmare/squad.xml', NightmareXML),
    ('/guardian/squad.xml', GuardianXML),
    ('/whiskey/squad.xml', WhiskeyXML),
    ('/toc/squad.xml', TOCXML),
], debug=True)
