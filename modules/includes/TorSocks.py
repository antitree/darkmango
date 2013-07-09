# TorSocks.py
# Description: Python Tor Module for natively making HTTP requests over Tor's SOCKS proxy
# Author: AntiTree
# Based on code from databigbang.com

import httplib
import socks
import urllib2
import TorCtl 
import TorUtil

class SocksiPyConnection(httplib.HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyHandler(urllib2.HTTPHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksiPyConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

class Tor():
	def __init__(self, host, ctrl_port, password=""):
		self.host = host
		self.ctrl_port = ctrl_port
		self.password = password
		TorUtil.loglevel = "NONE"

	def get_new_circuit(self):
		conn = TorCtl.connect(controlAddr=self.host, controlPort=self.ctrl_port, passphrase=self.password)
		conn.send_signal("NEWNYM")
		conn.close()

	def get_status(self):
	    try:
		conn = TorCtl.connect(controlAddr=self.host, controlPort=self.ctrl_port, passphrase=self.password)
		status = conn.is_live()
		conn.close()
	    except:
		pass
     	    return status
		
	def get_fast(self):
	    try:
		##this doesn't work anymore. It's been compiled into the Tor that you can't do this
		conn = TorCtl.connect(controlAddr=self.host, controlPort=self.ctrl_port, passphrase=self.password)
		conn.set_options([("FastFirstHop","0"),("EnforceDistinctSubnet","0"),("UseEntryGuards","0")])
		conn.send_signal("RELOAD")
		print(conn.get_info("circuit-status"))
		#, "EnforceDistinctSubnet":"0","UseEntryGuards":"0"})
		conn.close()
	    except:
		pass

class URLOpener():
	def __init__(self, socks_proxy_port, host='localhost'):
		self.socks_proxy_port = socks_proxy_port
		self.opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, host, self.socks_proxy_port))

	def get_url(self, url):
		try:
			h = self.opener.open(url)

			return h

		except urllib2.URLError, e:
			return e.code

#
