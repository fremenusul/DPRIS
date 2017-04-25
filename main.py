import webapp2
import jinja2
import os
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
            'soldiers' : soldier_data,

        }

        template = jinja_environment.get_template('soldier.html')
        self.response.out.write(template.render(template_values))
    def post(self):

        #TODO(Shangpo): Need to fix this to ensure each platoon can work.
        e = models.SoldierData(
            soldierName=self.request.get('name'),
            addedDate= datetime.datetime.now().date(),
            platoon = self.request.get('platoon')
        )
        e.put()

        #TODO(Shangpo): I need to fix this so I don't have to do a refresh.

        return self.redirect('/soldier')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/soldier', SoldierPage),
], debug=True)
