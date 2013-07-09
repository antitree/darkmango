#!/usr/bin/env python
#########################################################################
# Filename: spicymango.py
# Description: Main program for SpicyMango
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

import sys,time, sqlite3
from src.core import *

#Read code to dynamically call the name of this script.
execfile('src/getname')

#Print Banner
print ""
print " ___      _         __  __"                    
print "/ __|_ __(_)__ _  _|  \/  |__ _ _ _  __ _ ___" 
print "\__ \ '_ \ / _| || | |\/| / _` | ' \/ _` / _ \\"
print "|___/ .__/_\__|\_, |_|  |_\__,_|_||_\__, \___/"
print "    |_|        |__/                 |___/"     
print "The Open Source Intelligence Analysis Engine"
print ""
print "SpicyMango v1.0 Beta"
print "Copyright (C) 2011-2012 Chris Centore"
print "Written by: Chris Centore, Steve Swann, Jason Gunnoe"
print "Website: http://code.google.com/p/spicymango/"
print "Download: svn co http://spicymango.googlecode.com/svn/trunk/ spicymango/"
print "Licensed under the GNU AGPLv3"
print ""

#Redirect STDERR
sys.stderr = open('error.log', 'a')

# First setup configured output destinations
# If configured and doesn't exist, setup output file
if check_config("OUTPUT_FILE=") == 'ON':
	path = check_config("OUTPUT_FILE_NAME=")
	if not os.path.isfile(path):
		outputfile = file(path, "w")
		outputfile.close()

# If configured and doesn't exist, setup output DB
if check_config("OUTPUT_SQLITE3=") == 'ON':
	path = check_config("OUTPUT_SQLITE3_DB_PATH=")
	if not os.path.isfile(path):
		conn = sqlite3.connect(path)
		c = conn.cursor()
		c.execute('CREATE TABLE spicymango (modname TEXT, username TEXT COLLATE NOCASE, hostname TEXT COLLATE NOCASE, ircchan TEXT, msg TEXT COLLATE NOCASE, timeStamp DATE, hash TEXT, id INTEGER PRIMARY KEY)')
		c.execute('CREATE TABLE keywords (id INTEGER PRIMARY KEY, keyword TEXT, weight INTEGER, count INTEGER)')
		c.execute('CREATE TABLE alerts (id INTEGER, weight INTEGER)')
		c.execute('CREATE TABLE thresholds (tname TEXT, min INTEGER, max INTEGER)')
		c.execute("INSERT INTO thresholds VALUES('low',1,30)")
		c.execute("INSERT INTO thresholds VALUES('med',31,59)")
		c.execute("INSERT INTO thresholds VALUES('high',60,100)")
		c.execute('CREATE UNIQUE INDEX hashindex ON spicymango (hash)')
		conn.commit()
		conn.close()
	if not os.path.isfile("users.db"):
		conn = sqlite3.connect("users.db")
		c = conn.cursor()
		c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, isAdmin TEXT)")
		c.execute("INSERT INTO users VALUES(NULL,'admin','635b6a83deafb312c1c0aec4d9de940a','yes')")
		conn.commit()
		conn.close()

# Setup counter for determining how many modules are loaded at runtime.
mod_counter = 0

# Check to see which modules are enabled. Then run them.
enable_modirc = check_config("MOD_IRC=")
if enable_modirc == 'ON':
        import modules.mod_irc
	mod_counter += 1
enable_modtwitter = check_config("MOD_TWITTER=")
if enable_modtwitter == 'ON':
        import modules.mod_twitter
	mod_counter += 1
enable_modfacebook = check_config("MOD_FACEBOOK=")
if enable_modfacebook == 'ON':
        import modules.mod_facebook
	mod_counter += 1
enable_modrss = check_config("MOD_RSS=")
if enable_modrss == 'ON':
        import modules.mod_rss
	mod_counter += 1
enable_modgmail = check_config("MOD_GMAIL=")
if enable_modgmail == 'ON':
	import modules.mod_gmail
	mod_counter += 1
#If no modules are enabled in the config, error and exit.
if mod_counter == 0:
	print_warning(module,"No modules have been configured.")

# Run Web View if enabled in the config
enable_webview = check_config("WEB_VIEW=")
if enable_webview == 'ON':
	import web.web_view

# Let the program continue to run until an interrupt is recieved.
while 1:
        try:
                time.sleep(100000)
        except KeyboardInterrupt:
                print_warning(module,"Quiting SpicyMango...")
                sys.exit()
