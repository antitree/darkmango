#########################################################################
# Filename: mod_irc.py
# Description: This module connects to one or more IRC channels and listens
#              for keyword hits then writes those hits to the specified 
#              output.
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

import thread,sys,re,time
from includes import irc
sys.path.append("..")
from src.core import *
from src.output import *

#Read in code to dynamically get the name of the module.
execfile('src/getname')

def main():
	#Get parameters from config file
	irc_server = check_config("MOD_IRC_SERVER=")
	irc_channels = check_config("MOD_IRC_CHANNELS=")
	irc_user = check_config("MOD_IRC_USER=")

	def handle_state(newstate):
	    #If connected, join the channels listed in the config file
	    if newstate==4:
		channels = irc_channels.split(',')
		for channel in channels:
	        	MyConn.send_string("JOIN #" + channel)
			print_status(module,"Joined channel #" + channel)
	
	#Hanle for Raw input...can be used to debug module.
	def handle_raw(line):
	    print line

	def handle_parsed(prefix, command, params):
	    if command=="PRIVMSG":
		for keyword in keywords:
			hit = re.search(keyword[1], params[1])
			if hit:
				#If a match, send the output.
				modOutput = Output()
				modOutput.modname = module
				modOutput.username = prefix.split('!')[0]
				modOutput.hostname = prefix.split('@')[1]
				modOutput.ircchan = params[0]
				modOutput.msg = params[1]
				modOutput.send_output()
	    if command=="KICK":
			print_warning(module, "Uh oh, you have been kicked from " + params[0] + ". Waiting 60 seconds until attempting to rejoin.")
			time.sleep(60)
			MyConn.send_string("JOIN " + params[0])
			print_status(module,"Joined channel " + params[0])
       
	MyIRC=irc.IRC_Object( )
	MyConn=MyIRC.new_connection( )

	MyConn.nick=irc_user
	MyConn.ident=irc_user
	MyConn.server=(irc_server, 6667)
	MyConn.realname=irc_user

	MyConn.events['state'].add_listener(handle_state)
	#Enable to debug only
	#MyConn.events['raw'].add_listener(handle_raw)
	MyConn.events['parsed'].add_listener(handle_parsed)

	while 1:
		try:
			MyIRC.main_loop( )
		except Exception, err:
			log_error(module, keywords[0][1], str(err))
			sys.exit(1)

#Get keywords for module
keywords = get_keywords("mod_irc")
#Create a new thread for each keyword and run
if len(keywords) > 0:
	print_status(module,"loading...")
	thread.start_new_thread(main, ())
else:
	print_error(module, "No Keywords defined for this module")

