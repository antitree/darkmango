#########################################################################
# Filename: core.py
# Description: Core functions for SpicyMango.
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

import os,re,sys

#Read in code to dynamically get the name of this module.
execfile('src/getname')

# Print Colored Error Messages
def print_error(mod_name,msg):
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        print FAIL + "\n[!] Error: " + mod_name + ": " + msg + ENDC

# Print Colored Warning Messages
def print_warning(mod_name,msg):
        WARNING = '\033[93m'
        ENDC = '\033[0m'
        print WARNING + "\n[!] Warning: " + mod_name + ": " + msg + ENDC

# Print Status Messages
def print_status(mod_name,msg):
        print "[*] " + mod_name + ": " + msg


# Get configuation options from the config file.
def check_config(param):
	path = os.path.join(os.path.dirname(__file__), '..', 'config')
	try:
        	fileopen = file(path, "r")
	except:
		print_error(module,"Cannot find the configuration file.")
		sys.exit()
        # iterate through lines in file
        for line in fileopen:
		if not re.search('#.', line):
                	match = re.search(param, line)
                	if match:
                        	line = line.rstrip()
                        	line = line.replace('"', "")
                        	line = line.split("=")
                        	return line[1]

# Get Keyword/Module pairs from the keywords file.
def get_keywords(param):
        path = os.path.join(os.path.dirname(__file__), '..', 'keywords')
        try:
                fileopen = file(path, "r")
        except:
                print_error(module,"Cannot find keywords file. Make sure its in the spicymango directory.")
		sys.exit()
	wordlist = []
        # iterate through lines in file
        for line in fileopen:
                if not re.search('#.', line):
                        match = re.search(param, line)
                        if match:
				wordlist.append(eval(line))
        return wordlist

def get_feeds(param):
	path = os.path.join(os.path.dirname(__file__), '..', 'feeds')
        try:
                fileopen = file(path, "r")
        except:
                print_error(module,"Cannot find feeds file. Make sure its in the spicymango directory.")
                sys.exit()
        feedlist = []
        # iterate through lines in file
        for line in fileopen:
                if not re.search('^#.', line):
			match = re.search('http', line)
                	if match:
				feedlist.append(eval(line))
        return feedlist

def log_error(mod, keyword, error):
	import datetime
	sys.stderr.write('%s | %s | SEARCH_TERM: %s | ERROR: %s\n' % (datetime.datetime.now(), mod, keyword, error))
	print_error(mod, 'Keyword: %s - Thread exited with Error' % keyword)
