#########################################################################
# Filename: output.py
# Description: Defines functions for each output module.
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

import os,sys,datetime,time
from core import *
from string import printable

def rmNonprint(myStr):
	filtered_string = ''.join(filter(lambda x: x in printable, myStr))
	return filtered_string

class Output(object):
	#Define all attributes for module output
	modname = ''
	username = ''
	hostname = ''
	ircchan = ''
	msg = ''
	
	
	#Method to send output to various enabled destinations
	def send_output(self):
		#Method function for writing to a file
		def to_File():
			path = check_config("OUTPUT_FILE_NAME=")
			if not os.path.isfile(path):
				outputfile = file(path, "w")
			else:
				outputfile = file(path, "a")

			outString = str(datetime.datetime.now()) + ": " + rmNonprint(self.modname)
			if self.username != '':
				outString += ": " + rmNonprint(self.username)
			if self.hostname != '':
				outString += ": " + rmNonprint(self.hostname)
			if self.ircchan != '':
				outString += ": " + rmNonprint(self.ircchan)
			if self.msg != '':
				outString += ": " + rmNonprint(self.msg)
				outputfile.write(outString + "\n")
				outputfile.close()
		
		def to_Sqlite3():
			import sqlite3, hashlib, re
			
			# Generate hash to insert into the DB so only unique records get added.
			hash = hashlib.md5()
			hash.update(rmNonprint(self.modname))
			hash.update(rmNonprint(self.username))
			hash.update(rmNonprint(self.hostname))
			hash.update(rmNonprint(self.ircchan))
			hash.update(rmNonprint(self.msg))

			path = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(path)
			c = conn.cursor()
			sql = "INSERT INTO spicymango VALUES (?, ?, ?, ?, ?, ?, ?, NULL)"
			try:
				original = c.execute('SELECT COUNT(hash) FROM spicymango WHERE hash = ?', ([hash.hexdigest()])).fetchone()
				if original[0] is 0:
					c.execute(sql, (rmNonprint(self.modname), rmNonprint(self.username), rmNonprint(self.hostname), rmNonprint(self.ircchan), rmNonprint(self.msg), datetime.datetime.now(), hash.hexdigest()))
					event_id = c.execute('SELECT last_insert_rowid()').fetchone() 
					#Analysis
					keywords = c.execute('select * from keywords').fetchall()
					total_weight = 0
					#Iterate through keywords per event
					for keyword in keywords:
						event_total = rmNonprint(self.username) + " " + rmNonprint(self.ircchan) + " " + rmNonprint(self.msg)
						#find a match
						key_counter = 0
						if re.search(keyword[1], event_total, re.IGNORECASE):
							key_counter += 1
							c.execute('UPDATE keywords SET count = (count + ?) WHERE keyword = ?', (key_counter, keyword[1]))
							total_weight += keyword[2]
					if total_weight > 0:
						c.execute('INSERT INTO alerts VALUES(?, ?)', (event_id[0], total_weight))
			except sqlite3.OperationalError:
				print_error(module, "Database Locked...skipping record.")
			
			conn.commit()
			conn.close()
			                
		#Check config and send output where enabled, but first make sure required attributes are set.
		if self.modname is None:
			print_error("Output", "modname attribute must be defined in instance")
		
		#Counter var to determine if any ouput is enabled.
		output_count = 0
		
		file_enable = check_config("OUTPUT_FILE")
		if file_enable == "ON":
			to_File()
			output_count = 1
		sqlite3_enable = check_config("OUTPUT_SQLITE3=")
		if sqlite3_enable == "ON":
			to_Sqlite3()
			output_count = 1
		#If no output destinations are defined in config, send output to console
		if output_count == 0 or check_config("OUTPUT_CONSOLE=") == "ON":
			conString = ''
			if self.username != '':
				conString += ": " + rmNonprint(self.username)
			if self.hostname != '':
				conString += ": " + rmNonprint(self.hostname)
			if self.ircchan != '':
				conString += ": " + rmNonprint(self.ircchan)
			if self.msg != '':
				conString += ": " + rmNonprint(self.msg)

			print '\033[94m' + rmNonprint(self.modname) + ": " + '\033[0m' + str(datetime.datetime.now()) + conString
