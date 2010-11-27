import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import re

class GGClass(webapp.RequestHandler):
    def get(self):
        #print "hello all"
        libs = self.request.get_all("libs")
        js_pattern = re.compile(r"\.js$")
        google_scripts = []
        for lib in libs:
            if js_pattern.search(lib):
                str = "<script src='http://www.google.com/ig/f/%s'></script>" % lib
                google_scripts.append(str)
        #now output all google scripts
        self.response.headers['Content-Type'] = 'text/plain'
        for script in google_scripts:
            self.response.out.write(script)
        
        
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))
application = webapp.WSGIApplication(
                                     [('/gg.html', GGClass)],
                                     debug=True)
def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()