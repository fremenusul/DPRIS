import webapp2
import jinja2
import os
import logging
import calendar

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
        e = models.SoldierData(
            soldierName=self.request.get('name'),
            addedDate=datetime.datetime.now().date(),
            lastpromoted=datetime.datetime.now().date(),
            platoon=self.request.get('platoon'),
            rank='RCT'
        )
        e.put()

        return self.redirect('/soldier')


class DetailSoldier(webapp2.RequestHandler):
    def get(self):
        soldier_id = self.request.get('soldier')
        soldier_key = models.get_entity_from_url_safe_key(soldier_id)
        soldier_data = soldier_key
        #logging.info(soldier_data)

        template_values = {
            'soldier': soldier_data,

        }

        template = jinja_environment.get_template('detailsoldier.html')
        self.response.out.write(template.render(template_values))


class Attendance(webapp2.RequestHandler):
    def get(self):
        cal = calendar.Calendar()

        monthdates = [x for x in cal.itermonthdays(2017, 4) if x !=0]

        #logging.info(monthdates)

        template_values = {
            'monthdays' : monthdates
        }

        template = jinja_environment.get_template('attendance.html')
        self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
    ('/detailsoldier', DetailSoldier),
    ('/attendance', Attendance),
], debug=True)
