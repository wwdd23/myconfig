#encoding=utf-8
import urllib, urllib2, cookielib
import os

cookie = {"t": "590557c3fed2b9f7c4b3114c8a95f0fe8"}
# Get this session ID in Chrome: Right click page -> Inspect elements -> Resources
cookie = "".join(x + "=" + cookie[x] + ";" for x in cookie)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
urllib2.install_opener(opener)
req = urllib2.Request("http://www.renren.com/256593238/profile")
req.add_header('Cookie', cookie)
content = urllib2.urlopen(req).read()

with open("page.htm", "w") as f:
    f.write(content)
