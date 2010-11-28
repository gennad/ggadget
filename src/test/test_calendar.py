import unittest
from google.appengine.ext import webapp
from calendar import getSessionToken, getAuthSubUrl, parseSessionToken



class CalendarTest(unittest.TestCase):
    
    token=None
    
    def setUp(self):
        self.token="1/WBNaubPN3jacy5HJeP50Jlzr8IFXbjP0zb1rb24qZoE"
        
    
    """
    def testGetAuthSubUrl(self):
        r=getAuthSubUrl()
        print r
        self.assertNotEquals(None, r)
    
    def testParseSessionToken(self):
        s="http://localhost/welcome.pyc?auth_sub_scopes=https://www.google.com/calendar/feeds/&token=1/TQGTBJEARSTwXDUQh12vqyP_ErHtOg9NA-Wbko4sGxY"
        exp = "1/TQGTBJEARSTwXDUQh12vqyP_ErHtOg9NA-Wbko4sGxY"
        r = parseSessionToken(s)
        self.assertEquals(r, exp)
    """    
    def testGetSessionToken(self):
        getSessionToken(self.token)
        
        
        