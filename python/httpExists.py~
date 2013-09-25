import httplib, urlparse

def httpExists(url):
    host, path = urlparse.urlsplit(url)[1:3]
    if ':' in host:
        host, port = host.split(':', 1)
        try:
            port = int(port)
        except ValueError:
            print 'invalid port number %r' % (port,)
            return False
    else:
        port = None
    try:
          connection = httplib.HTTPConnection(host , port=port) 
          connection.request("HADE", path)
          resp = connection.getresponse()
          if resp.status == 200:
              found = True
          elif resp.status == 302:
              found = httpExists(urlparse.urljoin(url, resp.getheader('location','')) )
          else:
              print "Status %d%s:%s" %(resp.status, resp.reason, url)
              found = False
    except Exception, e:
        print e.__class__,e,url
        found = False
    return found
    
def _test():
        import doctest, httpExists
        return doctest.testmod(httpExists)
if __name__ == "__main__":
    _test()

        
