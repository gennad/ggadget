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
        js_pattern = re.compile(r".js$")
        google_scripts = []
        for lib in libs:
            if js_pattern.search(lib):
                if (lib.find(',')):
                    splitted_libs = lib.split(',')
                    for splitted_lib in splitted_libs:
                        str = "<script src='http://www.google.com/ig/f/%s'></script>" % splitted_lib
                        google_scripts.append(str)
                else:
                    str = "<script src='http://www.google.com/ig/f/%s'></script>" % splitted_lib
                    google_scripts.append(str)
                    
        #now output all google scripts
        self.response.headers['Content-Type'] = 'text/html'
        for script in google_scripts:
            #pass
            self.response.out.write(script)
            
        template_values = {
          'header': 'Github gadget',
        }
        path = os.path.join(os.path.dirname(__file__), 'templates')
        path = os.path.join(path, 'gadget.html')
        self.response.out.write(template.render(path, template_values))
        
        """
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))
        """
application = webapp.WSGIApplication(
                                     [('/gg.html', GGClass)],
                                     debug=True)
                                    
def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()