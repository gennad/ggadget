import unittest
from google.appengine.ext import webapp
from gg import GGClass, GithubAPI, DoLogin


class IndexTest(unittest.TestCase):
  
    def setUp(self):
        self.api = GithubAPI()
        application = webapp.WSGIApplication(
                                     [('/gg.html', GGClass), ('/dologin.html', DoLogin) ],
                                     debug=True)

    def test_get_user_feed(self):
        content =self.api.get_user_feed('gennad')
        self.assertNotEquals(None, content)
      

    def test_page_with_param(self):
        pass
  
    def  test_get_my_followers_followings(self):     
        r=self.api.get_my_followers_followings("gennad");
        self.assertNotEquals(None, r)

    def test_get_user_profile(self):
        r=self.api.get_user_profile("gennad")
        self.assertNotEquals(None, r)
        self.assertNotEquals(None, r.get_login())
        self.assertNotEquals(None, r.get_id()) 
        