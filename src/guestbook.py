'''
Created on 27.11.2010

@author: gennad
'''
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users

class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()

        if users.get_current_user():
            greeting.author = users.get_current_user()

            greeting.content = self.request.get('content')
            greeting.put()
            self.redirect('/')
          
class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)