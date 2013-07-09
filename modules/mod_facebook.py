#########################################################################
# Filename: mod_facebook.py
# Description: This module queries Facebook using its graph API and returns the
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
import json, urllib2, time

#Read in code to dynamically get the module name.
execfile('src/getname')

#Get configuration options
interval = int(check_config("MOD_FACEBOOK_INTERVAL="))

def main(query,*args):
	global interval
	while True:
		try:

			url = "http://graph.facebook.com/search?q=%s&type=post" % (query) 
			data = json.load(urllib2.urlopen(url))

			#Enable this print to see the raw data dump for troubleshooting
			#print json.dumps(data)

			for post in data['data']:
				if post['type'] == 'link':
					try:
						modOutput = Output()
						modOutput.modname = module
						modOutput.username = post['from']['name']
						modOutput.msg = post['message']
						modOutput.send_output()
					except KeyError:
						pass
		except Exception, err:
			log_error(module, query, str(err))
			sys.exit(1)

		#Set delay should be at least 5 seconds maybe more for facebook
		time.sleep(interval)

#Get keywords for module
keywords = get_keywords("mod_facebook")
#Create a new thread for each keyword and run
if len(keywords) > 0:
	print_status(module,"loading...")
	for keyword in keywords:
		thread.start_new_thread(main, (keyword[1],2))
else:
	print_error(module, "No Keywords defined for this module")

