#!/usr/bin/env python

import urllib
import urllib2
import cookielib

url_login = "http://www.renren.com/SysHome.do"
login_data = {"email":"13613112728","password":"075100"}


cj=cookielib.CookieJar()
opener = urllib2.build_opener( urllib2.HTTPBasicAuthHandler(cj))
resp = opener.open( url_login, urllib.urlencode(login_data))
