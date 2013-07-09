#########################################################################
# Filename: mod_rss.spy
# Description: This module reads RSS feeds from a text file
# Copyright (C) 2011-2012 Antitree
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or any later 
#    version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# SpicyMango written by: Chris Centore, Steve Swann, Jason Gunnoe
# Website: http://code.google.com/p/spicymango/
# Download: svn co http://spicymango.googlecode.com/svn/trunk/ spicymango/
#
#########################################################################

import thread,sys
sys.path.append("..")
from src.core import *
from src.output import *
import urllib2, urllib, time
from includes import feedparser
from includes import TorSocks
import re

#Read in code to dynamically get the module name.
execfile('src/getname')

#Get configuration options
interval = int(check_config("MOD_RSS_INTERVAL="))

def torup():
	global torhost, torport, torctlport, torpass
	torhost = check_config("TOR_HOST=")
	torport = int(check_config("TOR_PORT="))
	torctlport = int(check_config("TOR_CTL_PORT="))
	torpass = check_config("TOR_PASS=")

def main(query,keywords,tor,*args):
	global interval

	while True:
		try:
			author = ''
			desc = ''
			link = ''
			msg = ''


			url = query
			if tor == "ON":
				try:
					t = TorSocks.Tor(torhost, torctlport, torpass)
					if t.get_status():
						print_status(module, "Successfully connected to Tor")
					t.get_new_circuit()
					torconn = TorSocks.URLOpener(torport,torhost)

					feed = torconn.get_url(url)
					##TODO modify scraped results to remove HTTP requests of
					##  anonymized content
					#re.sub("http://", 'PROTECTED://',feed)
					#print(torconn.get_url("http://www.ifconfig.me/ip")).read()
				except Exception as e:
					print_error(module, "Error connecting to Tor. " +
						"make sure the control port is accessible, " + 
						"the SOCKS port is correct in your config file " +
						"and Tor is actually started. %s" % e)
					break
			else:
				feed = url

			rss = feedparser.parse(feed)
			print_status(module, 'Collecting feed %s...%s' % (url[0:15],url[-5:]))

			#Enable this print to see the raw data dump for troubleshooting
			#print rss

			try:
				for e in rss.entries:
					if "title" in e:
						title = e.title

					if "author" in e:
						author = e.author
					elif "authors" in e:
						author = e.authors
					
					if "summary_detail" in e:
						desc = e.summary_detail.value 
					elif "summary" in e:
						desc = e.summary

					if "link" in e:
						link = e.link
					elif "links" in e:
						link = e.links

					msg = title + ': ' + desc + '.\n' + link

					if re.search(keywords,msg):

						try:
							modOutput = Output()
							modOutput.modname = module
							modOutput.username = author
							modOutput.msg = msg
							modOutput.send_output()
						except KeyError:
							#pass
							print("Output error!!")
			except:
				print_error(module, "Could not parse url: %s  check to make sure it is a valid RSS or Atom feed" % url)
				break
		except Exception, err:
			log_error(module, feed, str(err))
			sys.exit(1)

		#Set delay should be at least an hour for RSS feeds
		time.sleep(interval)

#Get keywords for module
feeds = get_feeds("mod_rss")
#Create a new thread for each feed and run
if len(feeds) > 0:
	print_status(module,"loading...")
	for feed in feeds:
		if feed[2] == "ON":
			torup()
			TorSocks.Tor(torhost, torctlport, torpass).get_new_circuit()
			time.sleep(1) ##workaround to prevent the same circuits from being used
		thread.start_new_thread(main, (feed[0],feed[1],feed[2],2))

else:
	print_error(module, "No feeds defined for this module")

