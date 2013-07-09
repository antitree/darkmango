#########################################################################
# Filename: web_view.py
# Description: Invokes a stand-alone webserver to create an interactive
#		   GUI to SpicyMango.
# Copyright (C) 2011-2012 Chris Centore
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or any later 
#	version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# SpicyMango written by: Chris Centore, Steve Swann, Jason Gunnoe
# Website: http://code.google.com/p/spicymango/
# Download: svn co http://spicymango.googlecode.com/svn/trunk/ spicymango/
#
#########################################################################

import thread,sys
sys.path.append("..")
from src.bottle import route, run, template, static_file, request, response, redirect, post
from src.core import *
import sqlite3, datetime
from time import strftime
import json

#Read code to dynamically get name of this module.
execfile('src/getname')

def main():
	#Get config options
	ip = check_config("WEB_VIEW_IP=")
	port = check_config("WEB_VIEW_PORT=")
	
	#Route for the webroot
	@route('/')
	def mainview():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			#Get Thresholds
			lmax = conn.cursor().execute("SELECT max from thresholds WHERE tname = 'low'").fetchone()
			med = conn.cursor().execute("SELECT min,max from thresholds WHERE tname = 'med'").fetchone()
			hmin = conn.cursor().execute("SELECT min from thresholds WHERE tname = 'high'").fetchone()

			events = conn.cursor().execute('select count(id) from spicymango').fetchone()
			high_events = conn.cursor().execute('select count(id) from alerts where weight >= ?', (hmin[0],)).fetchone()
			medium_events = conn.cursor().execute('select count(id) from alerts where weight between ? and ?', (med[0],med[1])).fetchone()
			low_events = conn.cursor().execute('select count(id) from alerts where weight <= ?', (lmax[0],)).fetchone()
			chart_highs = conn.cursor().execute("select count(s.id), strftime('%H', s.timeStamp) from spicymango s join alerts a on s.id = a.id where a.weight >= ? and s.timeStamp >= datetime('now', 'localtime', '-12 hour') group by strftime('%H', s.timeStamp)", (hmin[0],)).fetchall()
			chart_mediums = conn.cursor().execute("select count(s.id), strftime('%H', s.timeStamp) from spicymango s join alerts a on s.id = a.id where a.weight between ? and ? and s.timeStamp >= datetime('now', 'localtime', '-12 hour') group by strftime('%H', s.timeStamp)", (med[0],med[1])).fetchall()
			chart_lows = conn.cursor().execute("select count(s.id), strftime('%H', s.timeStamp) from spicymango s join alerts a on s.id = a.id where a.weight <= ? and s.timeStamp >= datetime('now', 'localtime', '-12 hour') group by strftime('%H', s.timeStamp)", (lmax[0],)).fetchall()
			recent_alls = conn.cursor().execute("select a.weight, s.msg, s.timeStamp, s.id from spicymango s join alerts a on s.id=a.id order by timeStamp DESC limit 7").fetchall()
			recent_highs = conn.cursor().execute("select s.msg, s.timeStamp, s.id from spicymango s join alerts a on s.id=a.id where a.weight >= ? order by timeStamp DESC limit 7", (hmin[0],)).fetchall()
			recent_mediums = conn.cursor().execute("select s.msg, s.timeStamp, s.id from spicymango s join alerts a on s.id=a.id where a.weight between ? and ? order by timeStamp DESC limit 7", (med[0],med[1])).fetchall()
			recent_lows = conn.cursor().execute("select s.msg, s.timeStamp, s.id from spicymango s join alerts a on s.id=a.id where a.weight <= ? order by timeStamp DESC limit 7", (lmax[0],)).fetchall()
			top_users = conn.cursor().execute("select s.username, count(s.username) from spicymango s join alerts a on s.id = a.id group by username order by count(username) DESC LIMIT 5").fetchall()
			top_alerts = conn.cursor().execute("select s.msg, a.weight, s.id from spicymango s join alerts a on s.id = a.id order by a.weight DESC LIMIT 5").fetchall()
			top_keywords = conn.cursor().execute("select keyword, count from keywords order by count DESC LIMIT 5").fetchall()
			conn.close()
			
			i = 0
			last_12 = []
			while i < 13:
				d = datetime.datetime.now() - datetime.timedelta(hours=i)
				hr = d.strftime("%H")
				last_12.append(hr)
				i += 1

			last_12.reverse()
			c_hours = ""
			c_highs = ""
			c_mediums = ""
			c_lows = ""
			for hour in last_12:
				high_count = "0"
				medium_count = "0"
				low_count = "0"
				for chigh in chart_highs:
					if hour == chigh[1]:
						high_count = str(chigh[0])
				for cmedium in chart_mediums:
					if hour == cmedium[1]:
						medium_count = str(cmedium[0])
				for clow in chart_lows:
					if hour == clow[1]:
						low_count = str(clow[0])
				c_hours = c_hours + "<th>"+hour+":00</th>"
				c_highs = c_highs + "<td>"+high_count+"</td>"
				c_mediums = c_mediums + "<td>"+medium_count+"</td>"
				c_lows = c_lows + "<td>"+low_count+"</td>"
			r_all = ""
			r_high = ""
			r_medium = ""
			r_low = ""
			for rall in recent_alls:
				if rall[0] >= hmin[0]:
					priority = "high"
					priority_label = "High"
				if med[0] <= rall[0] <= med[1]:
					priority = "medium"
					priority_label = "Medium"
				if rall[0] <= lmax[0]:
					priority = "low"
					priority_label = "Low"
					
				r_all = r_all + "<tr><td><span class='ticket {!s}'>{!s}</span></td><td class='full'><a id='{!s}' href='javascript:void(0)'>{!s}</a></td><td class='who'>{!s}</td></tr>".format(priority, priority_label, rall[3], rall[1], rall[2])
			for rhigh in recent_highs:
				r_high = r_high + "<tr><td><span class='ticket high'>High</span></td><td class='full'><a id='{!s}' href='javascript:void(0)'>{!s}</a></td><td class='who'>{!s}</td></tr>".format(rhigh[2],rhigh[0], rhigh[1])
			for rmedium in recent_mediums:
				r_medium = r_medium + "<tr><td><span class='ticket medium'>Medium</span></td><td class='full'><a id='{!s}' href='javascript:void(0)'>{!s}</a></td><td class='who'>{!s}</td></tr>".format(rmedium[2], rmedium[0], rmedium[1])
			for rlow in recent_lows:
				r_low = r_low + "<tr><td><span class='ticket low'>Low</span></td><td class='full'><a id='{!s}' href='javascript:void(0)'>{!s}</a></td><td class='who'>{!s}</td></tr>".format(rlow[2], rlow[0], rlow[1])
				
			return template('webview', eventcount=events[0], highs=high_events[0], mediums=medium_events[0], lows=low_events[0], chart_hours=c_hours, chart_highs=c_highs, chart_mediums=c_mediums, chart_lows=c_lows, recent_all=r_all, recent_highs=r_high, recent_mediums=r_medium, recent_lows=r_low, topusers=top_users, topalerts=top_alerts, topkeywords=top_keywords)
		else:
			redirect('/login')

	#Route for Dashboard Detail
	@route('/dash-detail')
	def dash():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			if request.query.get('type') == "recent":
				event_id = request.query.get('eid')
				event = conn.cursor().execute("SELECT s.modname, s.timeStamp, a.weight, s.username, s.hostname, s.ircchan, s.msg FROM spicymango s JOIN alerts a ON s.id = a.id WHERE s.id = ?",(event_id,)).fetchone()
				conn.close()
				return "<tr><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td></tr>".format(event[0],event[1],event[2],event[3],event[4],event[5],event[6])
			if request.query.get('type') == "topuser":
				user = request.query.get('username')
				events = conn.cursor().execute("SELECT s.modname, s.timeStamp, a.weight, s.hostname, s.ircchan, s.msg FROM spicymango s JOIN alerts a ON s.id = a.id WHERE s.username = ? ORDER BY s.timeStamp DESC LIMIT 10",(user,)).fetchall()
				conn.close()
				results = ""
				for event in events:
					results = results + "<tr><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td><td>{!s}</td></tr>".format(event[0],event[1],event[2],event[3],event[4],event[5])
				return results 
	
	#Routes for Login
	@route('/login')
	def login():
		action = request.query.action
		if action == "logout":
			my_notice = "Logged Out"
			response.delete_cookie("loggedin")
		elif action == "error":
			my_notice = "Username or Password Incorrect"
		else:
			my_notice = ""
		return template('login', notice=my_notice)	
	
	@post('/login-check')
	def logincheck():
		import hashlib
		if request.forms.get("login_user") and request.forms.get("login_password"):
			user = request.forms.get("login_user")
			password = hashlib.md5(request.forms.get("login_password")).hexdigest()

			database = "users.db"
			conn = sqlite3.connect(database)
			isUser = conn.cursor().execute("SELECT COUNT(username) FROM users WHERE username = ? and password = ?", (user,password)).fetchone()
			conn.close()

			if isUser[0] == 1:
				response.set_cookie("loggedin", request.forms.get('login_user'), secret='sm2345-45634')
				if request.forms.get("remember") and request.forms.get("remember") == "yes":
					exp = datetime.datetime(2025, 1, 1, 00, 00, 00)
					response.set_cookie("remember", request.forms.get('login_user'), expires=exp)
				else:
					response.delete_cookie("remember")
				redirect('/')
			else:
				redirect('/login?action=error')

	#Route for Events
	@route('/events')
	def eventpage():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			return template('events')
		else:
			redirect('/login')
	
	#Route for AJAX Events
	@route('/events.txt')
	def eventpage():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			rows = conn.cursor().execute("select modname, timeStamp, username, msg from spicymango order by timeStamp DESC").fetchall()
			conn.close()
			
			json_events = {}
			json_events['aaData'] = []
			
			for row in rows:
				json_events['aaData'].append([row[0], row[1], row[2], row[3]])
		
			response.set_header('Content-type', 'application/json')
			return json.dumps(json_events, indent=4)

	#Route for Alerts
	@route('/alerts')
	def eventpage():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			#Get Thresholds
			lmax = conn.cursor().execute("SELECT max from thresholds WHERE tname = 'low'").fetchone()
			med = conn.cursor().execute("SELECT min,max from thresholds WHERE tname = 'med'").fetchone()
			hmin = conn.cursor().execute("SELECT min from thresholds WHERE tname = 'high'").fetchone()

			alows = conn.cursor().execute("select count(id) from alerts where weight <= ?", (lmax[0],)).fetchone() 
			amediums = conn.cursor().execute("select count(id) from alerts where weight between ? and ?", (med[0],med[1])).fetchone() 
			ahighs = conn.cursor().execute("select count(id) from alerts where weight >= ?", (hmin[0],)).fetchone() 
			conn.close()
			return template('alerts', total_alert_highs=ahighs[0], total_alert_mediums=amediums[0], total_alert_lows=alows[0])
		else:
			redirect('/login')

	#Route for AJAX Alerts
	@route('/alerts.txt')
	def eventpage():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			#Get Thresholds
			lmax = conn.cursor().execute("SELECT max from thresholds WHERE tname = 'low'").fetchone()
			med = conn.cursor().execute("SELECT min,max from thresholds WHERE tname = 'med'").fetchone()
			hmin = conn.cursor().execute("SELECT min from thresholds WHERE tname = 'high'").fetchone()

			rows = conn.cursor().execute("select a.weight, s.modname, s.timeStamp, s.username, s.msg from spicymango s join alerts a on s.id=a.id").fetchall()
			conn.close()
			
			json_alerts = {}
			json_alerts['aaData'] = []

			for row in rows:
				if row[0] <= lmax[0]:
					priority = "Low"
					tdclass = "low"
				if med[0] <= row[0] <= med[1]:
					priority = "Medium"
					tdclass = "medium"
				if row[0] >= hmin[0]:
					priority = "High"
					tdclass = "high"
				
				total_weight = "<span class=\'ticket "+tdclass+"\'>"+priority+"</span>"
				json_alerts['aaData'].append([total_weight, row[0], row[1], row[2], row[3], row[4]])

			response.set_header('Content-type', 'application/json')
			return json.dumps(json_alerts, indent=4)

	#Route for Password Change
	@route('/set-password')
	def set_pass():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			return template('set-password')
		else:
			redirect('/login')
	
	#Route for AJAX Password Change
	@post('/setpass')
	def pass_set():
		import hashlib
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			cpass = hashlib.md5(request.forms.get('currentpass')).hexdigest()
			npass = hashlib.md5(request.forms.get('newpass')).hexdigest()

			database = "users.db" 
			conn = sqlite3.connect(database)
			
			if conn.cursor().execute("SELECT COUNT(username) from users WHERE password = ?", (cpass,)).fetchone()[0] == 1:
				conn.cursor().execute("UPDATE users SET password = ? WHERE password = ?", (npass,cpass))
				conn.commit()
				conn.close()
				response.delete_cookie("loggedin")
				return "1"
			else:
				conn.close()
				return "2"
	
	#Route for Keywords
	@route('/set-keywords')
	def keywordspage():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			lmax = conn.cursor().execute("select max from thresholds where tname = \'low\'").fetchone()
			hmin = conn.cursor().execute("select min from thresholds where tname = \'high\'").fetchone()
			sliderp = "[%s,%s]," % (lmax[0],hmin[0])
			rows = conn.cursor().execute("select id, keyword, weight from keywords order by weight DESC").fetchall()
			conn.close()
			trRows = ""
	
			for row in rows:
				trRows = trRows + '<tr id=\'%s\'><td>%s</td><td>%s</td></tr>' % (row[0],row[1],row[2])

			return template('set-keywords', dataRows=trRows, slider=sliderp)
		else:
			redirect('/login')

	#Route for Keyword Updates
	@post('/keyupdate')
	def updatekey():
			username = request.get_cookie("loggedin", secret='sm2345-45634')
			if username:
				rid = request.forms.get('id')
				rvalue = request.forms.get('value')
				rcolumn = request.forms.get('columnName')
				database = check_config("OUTPUT_SQLITE3_DB_PATH=")
				conn = sqlite3.connect(database)
				if rcolumn == "keyword":
					conn.cursor().execute('UPDATE keywords SET keyword = ?, count = 0 WHERE id = ?', (rvalue, rid))
					conn.commit()
					conn.close()
				elif rcolumn == "weight":	
					conn.cursor().execute('UPDATE keywords SET weight = ? WHERE id = ?', (rvalue, rid))
					conn.commit()
					conn.close()
				else:
					return "Error"
				return rvalue
	
	#Route for Keyword Add
	@post('/keyadd')
	def addkey():
			username = request.get_cookie("loggedin", secret='sm2345-45634')
			if username:
				rkeyword = request.forms.get('keyword')
				rweight = request.forms.get('weight')
				database = check_config("OUTPUT_SQLITE3_DB_PATH=")
				conn = sqlite3.connect(database)
				conn.cursor().execute('INSERT INTO keywords VALUES(NULL,?,?,0)', (rkeyword, rweight))
				rid = conn.cursor().execute('SELECT last_insert_rowid()').fetchone()
				conn.commit()
				conn.close()

				return str(rid[0])
	
	#Route for Keyword Delete
	@post('/keydelete')
	def deletekey():
			username = request.get_cookie("loggedin", secret='sm2345-45634')
			if username:
				rid = request.forms.get('id')
				database = check_config("OUTPUT_SQLITE3_DB_PATH=")
				conn = sqlite3.connect(database)
				conn.cursor().execute('DELETE from keywords WHERE id = ?', (rid))
				conn.commit()
				conn.close()

				return 'ok'

	#Route for ReAnalyze
	@route('/reAnalyze')
	def analyze():
		#Analysis
		database = check_config("OUTPUT_SQLITE3_DB_PATH=")
		conn = sqlite3.connect(database)
		conn.cursor().execute('DELETE from alerts')
		conn.cursor().execute('UPDATE keywords SET count = 0')

		events = conn.cursor().execute('SELECT username,ircchan,msg,id from spicymango').fetchall()
		keywords = conn.cursor().execute('SELECT * from keywords').fetchall()
		
		#Iterate through Events
		for event in events:
			total_event = event[0] + " " + event[1] + " " + event[2]
			total_weight = 0
			#Iterate through keywords per event
			for keyword in keywords:
				#find a match
				key_counter = 0
				if re.search(keyword[1], total_event, re.IGNORECASE):
					key_counter += 1
					conn.cursor().execute('UPDATE keywords SET count = (count + ?) WHERE keyword = ?', (key_counter, keyword[1]))
					total_weight += keyword[2]
			if total_weight > 0:
				conn.cursor().execute('INSERT INTO alerts VALUES(?, ?)', (event[3], total_weight))
		conn.commit()
		conn.close()
		return '1'

	#Route for Threshold
	@route('/thresholdsave')
	def tsave():
		username = request.get_cookie("loggedin", secret='sm2345-45634')
		if username:
			lmax = (request.query.get('lmax'),)
			mmin = request.query.get('mmin')
			mmax = request.query.get('mmax')
			hmin = (request.query.get('hmin'),)
			database = check_config("OUTPUT_SQLITE3_DB_PATH=")
			conn = sqlite3.connect(database)
			conn.cursor().execute('UPDATE thresholds SET max = ? WHERE tname = \'low\'', lmax)
			conn.cursor().execute('UPDATE thresholds SET min = ?, max = ? WHERE tname = \'med\'', (mmin, mmax))
			conn.cursor().execute('UPDATE thresholds SET min = ? WHERE tname = \'high\'', hmin)
			conn.commit()
			conn.close()
			return '1'
		else: 
			return 'Error'

	#Route for png images
	@route('/images/:filename#.*\.png#')
	def send_image(filename):
		return static_file(filename, root='web/images/', mimetype='image/png')

	#Route for jpg images
	@route('/images/:filename#.*\.jpg#')
	def send_image(filename):
		return static_file(filename, root='web/images/', mimetype='image/jpg')
	
	#Route for style sheets
	@route('/css/:filename#.*\.css#')
	def send_image(filename):
		return static_file(filename, root='web/css/')

	#Route for javascript
	@route('/js/:filename#.*\.js#')
	def send_image(filename):
		return static_file(filename, root='web/js/')

	#Route for HTML
	@route('/:filename#.*\.html#')
	def send_image(filename):
		return static_file(filename, root='web/')


	# Run Web View webserver on specified ip and port
	print_status(module,"Connect to http://%s:%s" % (ip, port))
	run(port=port, host=ip, quiet="True")

#If the output file option is not set in the config, don't run.
check_outputsqlitedb = check_config("OUTPUT_SQLITE3")
if check_outputsqlitedb == "ON":
	print_status(module,"loading...")
	thread.start_new_thread(main, ())
else:
	print_error(module,"Cannot start, no database configured.")
