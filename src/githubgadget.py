'''
Created on 27.11.2010

@author: gennad
'''
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from guestbook import Greeting, Guestbook

class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
          'greetings': greetings,
          'url': url,
          'url_linktext': url_linktext,
          }
        path = os.path.join(os.path.dirname(__file__), 'templates')
        path = os.path.join(path, 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
if __name__ == "__main__":
    main()