# -*- coding: utf-8 -*-


import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import re

import urllib2
import sys
import re
import base64
from urlparse import urlparse
import yaml

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
            #self.response.out.write(script)
            pass
            
            
        template_values = {
          'google_scripts': ''.join(google_scripts),
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
        
class GithubAPI:
    """
    Cleans the keys.
    
    It needs because github sends with keys like :name
    @param dict: Dictionary to cleanup
    @return: Dictionary
    """
    def cleanup_dict(self, dict):
        for repo in dict:
                for key in repo:
                    if key[0] == ':':
                        new_key = key[1:]
                        repo[new_key] = repo.pop(key)
        return dict
        
    """
    Returns the list of watched repos
    """
    def get_watched_repos(self, login):
        url = "http://github.com/api/v2/yaml/repos/watched/%s" % login
        repos = None
        try:
            response = urllib2.urlopen(url)
            content = response.read()
            dict = yaml.load(content)
            repos = dict.get('repositories')
        except urllib2.URLError, e:
            pass
        except Exception, e1:
            pass
        return repos
            
        """
        Content of repos
        url = repo['url']
        created = repo['created_at']
        forks = repo['forks']
        is_fork = repos['fork']
        owner = repos['owner']
        watchers = repos['watchers']
        open_issues = repos['open_issues']
        is_private = repos['private']
        homepage = repos['homepage']
        desc = repos['description']
        name = repos['name']
        pushed_at = repos['pushed_at']
        """    
                
    def get_my_repos(self, login):
        url = "http://github.com/api/v2/yaml/repos/show/%s" % login
        repos = None
        try:
            response = urllib2.urlopen(url)
            content = response.read()
            dict = yaml.load(content)
            repos = dict.get('repositories')
        except urllib2.URLError, e:
            pass
        except Exception, e1:
            pass
        return repos
    
    def get_my_profile(self, login):
        url = "http://github.com/api/v2/yaml/user/show/%s" % login
        dict = None
        try:
            response = urllib2.urlopen(url)
            content = response.read()
            dict = yaml.load(content)
        except urllib2.URLError, e:
            pass
        except Exception, e1:
            pass
        return dict
    
    def get_my_followers_followings(self, login):
        followings_url = "http://github.com/api/v2/yaml/user/show/%s/followers" % login
        followers_url = "http://github.com/api/v2/yaml/user/show/%s/followers" % login
        try:
            response = urllib2.urlopen(followers_url)
            content = response.read()
            followers_dict = yaml.load(content)
            
            response = urllib2.urlopen(followings_url)
            content = response.read()
            followings_dict = yaml.load(content)
        except urllib2.URLError, e:
            pass
        except Exception, e1:
            pass
        return followers_dict, followings_dict

class DoLogin(webapp.RequestHandler):
    #static variable
    url = 'http://github.com/api/v2/json'
    #private variables
    __login = None
    
    __password = None
    
    
    def generate_show_user_link(self, login):
        str = self.url+'/user/show/'+login
        return str
    
    def set_password(self, password):
        self.__password = password
    def get_password(self):
        return self.__password
    def get_login(self):
        return self.__login
    def set_login(self, login):
        self.__login = login
    login = property(get_login, set_login)    
    password = property(get_password, set_password)
    def post(self):
        login = self.request.get("login", '')
        password = self.request.get("pass", '')
        if login == '' or password == '':
            pass 
        else:
            self.login = login
            self.password = password
            
            #self.send_auth()
            api = GithubAPI()
            
            repos = api.get_watched_repos(login)
            api.cleanup_dict(repos)
            
                
            """
            a = {'name': 'greg', 'value': 'val'}
            b = {'name': 'greg2', 'value': 'val2'}
            repos = [a, b]
            """
            if repos != None:
                
                """
                for repo in repos:
                    name = repo[':name']
                    s = ""
                """
                template_values = {
                    'repos': repos,
                    'header': 'Watched repositories',
                }
                path = os.path.join(os.path.dirname(__file__), 'templates')
                path = os.path.join(path, 'watched_repos.html')
                self.response.out.write(template.render(path, template_values))
            
    def send_auth(self):
        theurl = self.generate_show_user_link(self.__login)
        # if you want to run this example you'll need to supply
        # a protected page with your username and password

        req = urllib2.Request(theurl)
        handle = None
        try:
            handle = urllib2.urlopen(req)
        except IOError, e:
            # here we *want* to fail
            pass
        else:
            # If we don't fail then the page isn't protected
            #print "This page isn't protected by authentication."
            #sys.exit(1)
            pass
        e = handle
        if not hasattr(e, 'code') or e.code != 401:
            # we got an error - but not a 401 error
            print "This page isn't protected by authentication."
            print 'But we failed for another reason.'
            sys.exit(1)

        authline = e.headers['www-authenticate']
        # this gets the www-authenticate line from the headers
        # which has the authentication scheme and realm in it


        authobj = re.compile(
            r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
            re.IGNORECASE)
        # this regular expression is used to extract scheme and realm
        matchobj = authobj.match(authline)

        if not matchobj:
            # if the authline isn't matched by the regular expression
            # then something is wrong
            print 'The authentication header is badly formed.'
            print authline
            sys.exit(1)

        scheme = matchobj.group(1)
        realm = matchobj.group(2)
        # here we've extracted the scheme
        # and the realm from the header
        if scheme.lower() != 'basic':
            print 'This example only works with BASIC authentication.'
            sys.exit(1)

        base64string = base64.encodestring(
                '%s:%s' % (self.__login, self.__password))[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header("Authorization", authheader)
        try:
            handle = urllib2.urlopen(req)
        except IOError, e:
            # here we shouldn't fail if the username/password is right
            print "It looks like the username or password is wrong."
            sys.exit(1)
        thepage = handle.read()
        
    def send_auth_passwd_mgr(self):
        theurl = 'http://www.someserver.com/toplevelurl/somepage.htm'
        username = 'johnny'
        password = 'XXXXXX'
        # a great password

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        passman.add_password(None, theurl, username, password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url

        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # create the AuthHandler

        opener = urllib2.build_opener(authhandler)

        urllib2.install_opener(opener)
        # All calls to urllib2.urlopen will now use our handler
        # Make sure not to include the protocol in with the URL, or
        # HTTPPasswordMgrWithDefaultRealm will be very confused.
        # You must (of course) use it when fetching the page though.
        
        pagehandle = urllib2.urlopen(theurl)
        # authentication is now handled automatically for us

application = webapp.WSGIApplication(
                                     [('/gg.html', GGClass), ('/dologin.html', DoLogin) ],
                                     debug=True)
                                    
def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
    
