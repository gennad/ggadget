import unittest
from google.appengine.ext import webapp
from gg import GGClass, GithubAPI
from gg import DoLogin

class IndexTest(unittest.TestCase):
  
  def setUp(self):
      application = webapp.WSGIApplication(
                                     [('/gg.html', GGClass), ('/dologin.html', DoLogin) ],
                                     debug=True)

  def test_get_user_feed(self):
      api = GithubAPI()
      content = api.get_user_feed('gennad')
      self.assertNotEquals(None, content)
      

  def test_page_with_param(self):
      pass
