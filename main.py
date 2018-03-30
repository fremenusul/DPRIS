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
                memcache.set(platoon, soldier_data, 10)

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
            'prevRank': demote,

        }

        template = jinja_environment.get_template('detailsoldier.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        if self.request.get('action') == 'promotepv2':
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
    ('/viking/squad.xml', VikingXML),
    ('/nightmare/squad.xml', NightmareXML),
    ('/guardian/squad.xml', GuardianXML),
    ('/whiskey/squad.xml', WhiskeyXML),
    ('/toc/squad.xml', TOCXML),
], debug=True)
