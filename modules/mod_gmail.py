#########################################################################
# Filename: mod_gmail.py
# Description: This module reads email from a gmail account via IMAP. It
#	       support keywords searches and looking for specific senders
# Copyright (C) 2011-2012 AntiTree
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
import imaplib, email
#import json, urllib2, urllib, time

#Read in code to dynamically get the module name.
execfile('src/getname')

#Get configuration options
interval = int(check_config("MOD_GMAIL_INTERVAL="))
gmail = check_config("MOD_GMAIL_EMAIL=")
password  = check_config("MOD_GMAIL_PASSWORD=")

def main(gmail, password, mailbox, *args):
	global interval
	while True:
		try:
			body = ""
			try: 
				mail = imaplib.IMAP4_SSL('imap.gmail.com')
				mail.login(gmail, password)
			except:
				print_error(module, "Connection reset by gmail...will try again in %d seconds" % interval)
				time.sleep(interval)
				continue
			try: 
				mail.select(mailbox)
				result, data = mail.uid('search', None, '(UNSEEN)') 
			except:
				log_error(module, mailbox, "Incorrect mailbox named: %s" % mailbox)
				sys.exit(1)

			uids = data[0].split()
			if not len(uids) > 0:
				print_status(module, "No new emails in %s mailbox." % mailbox)
				time.sleep(interval)
				continue
			print_status(module, "Downloading %s messages from %s mailbox" % (len(uids), mailbox))
			csv = ",".join(uids) ##TODO: switch this back to a single loop
			result, msgs = mail.uid('fetch', csv, '(RFC822)')
			for msg in msgs:
				for e in msg:
					eml = email.message_from_string(e)
					maintype = eml.get_content_maintype()
					if maintype == 'multipart':
						for part in eml.get_payload():
							if part.get_content_maintype() == 'text':
								body = part.get_payload()
					elif maintype == 'text':
						body = eml.get_payload()

				if len(body) > 5 and 'RFC822' not in body: ##TODO: fix very hacky
					try:
						modOutput = Output()
						modOutput.modname = module
						modOutput.username = eml['From']
						modOutput.msg = body
						modOutput.send_output()
					except KeyError:
						print_error(module, 'Error collecting email')
						pass
			mail.logout()
		except Exception, err:
			log_error(module, mailbox, str(err))
			sys.exit(1)

		#Set delay should be at least 5 seconds maybe more for facebook
		time.sleep(interval)

#Get mailboxes for module
keywords = get_keywords("mod_gmail")
#Create a new thread for each mailbox and run
if len(keywords) > 0:
	print_status(module,"loading...")
	for keyword in keywords:
		thread.start_new_thread(main, (gmail, password, keyword[1],2))
else:
	print_error(module, "No mailboxes defined for this module")

