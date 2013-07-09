#########################################################################
# Filename: mod_twitter.py
# Description: This module queries Twitter using its API and returns the
#              results to the specified output.  
# Copyright (C) 2011-2012 Chris Centore
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
from xml.dom import minidom
from xml.parsers import expat
import time, urllib

#Read in code to dynamically get the module name.
execfile('src/getname')

#Get configuration options
count = check_config("MOD_TWITTER_COUNT=")
interval = int(check_config("MOD_TWITTER_INTERVAL="))

def main(query,*args):
	id = 0
	global count, interval
	while True:

		try:
			url = "http://search.twitter.com/search.atom?rpp=" + count + "&q=%s&since_id=%s" % (query, id)
			xml = urllib.urlopen(url)
			doc = minidom.parse(xml)
			entries = doc.getElementsByTagName("entry")

			if len(entries) > 0:
				entries.reverse()
				#If entries, interate through entries and output results.
				for e in entries:
					title = e.getElementsByTagName("title")[0].firstChild.data.replace("\n", "")
					pub = e.getElementsByTagName("published")[0].firstChild.data
					id = e.getElementsByTagName("id")[0].firstChild.data.split(":")[2]
					name = e.getElementsByTagName("name")[0].firstChild.data.split(" ")[0]
					#Try output...non-ascii will throw an exception otherwise.
					try:
						modOutput = Output()
						modOutput.modname = module
						modOutput.username = name
						modOutput.msg = title
						modOutput.send_output()
					except UnicodeEncodeError:
						pass
						#print_warning(module, "Couldn't print line because it contains non-ASCII values.
		except expat.ExpatError:
			print_warning(module, "Rate limit exceeded...delaying 120 seconds.")
			time.sleep(120)
		except Exception, err:
			log_error(module, query, str(err))
			sys.exit(1)

		#Set delay should be at least 5 seconds.
		time.sleep(interval)

#Get keywords for module
keywords = get_keywords("mod_twitter")
#Create a new thread for each keyword and run
if len(keywords) > 0:
	print_status(module,"loading...")
	for keyword in keywords:
		thread.start_new_thread(main, (keyword[1],2))
else:
	print_error(module, "No Keywords defined for this module")
