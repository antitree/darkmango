# Python IRC Module, by Maurits Dijkstra
# irc.py - global and connection classes 

import sys
import select
import socket
import string
import imp

class IRC_Object:
	def __init__(self):
		self.connections=[]
		self.extensions=[]
		self.fds_read=[]
		self.fds_write=[]
		self.active=None

	def new_connection(self):
		newconn=IRC_Connection()
		self.connections.append(newconn)
		for extension in self.extensions:
			extension.initialize_connection(newconn)		

		return newconn

	def main_loop(self):
		self.fds_read=[]
		self.fds_write=[]

		for connection in self.connections:
			if connection.state > 1:
				self.fds_read.append(connection.socket)			
				self.fds_write.append(connection.socket)			
		
		if len(self.fds_read)!=0:
			select.select(self.fds_read, [], [], 0.25)
		if len(self.fds_write)!=0:
			select.select([], self.fds_write, [], 0.5)
		
		for connection in self.connections:
			if self.fds_read.count(connection.socket) > 0:
				connection.fd_status[0]=1				
			if self.fds_write.count(connection.socket) > 0:
				connection.fd_status[1]=1
			
			self.active=connection
			connection.main_loop()
			
			connection.fd_status=[0, 0]
		self.active=None

	def load_extension(self, name):
		extension=None

		try:
			sys.modules[name]
		except KeyError:
			pass
		else:
			return

		fp, pathname, description=imp.find_module(name)

		try:
			extension=imp.load_module(name, fp, pathname, description)
		finally:
			# Since we may exit via an exception, close fp explicitly.
			if fp:
				fp.close()					
		
		if extension:
			for dependency in extension.dependencies:
				self.load_extension(dependency)
			
			self.extensions.append(extension)
			
			extension.initialize()
			extension.IRC_Instance=self
			for connection in self.connections:
				extension.initialize_connection(connection)

class IRC_Connection:
	def __init__(self):
		# State values:
		# -1: disconnected, do nothing
		#  0: disconnected, get socket
		#  1: got socket, connect
		#  2: connected, send login
		#  3: sent login, wait for '001' (return PING)
		#  4: logged in
		self.state=0
		self.socket=None
		self.sendbuffer=""
		self.readbuffer=""
		self.fd_status=[0, 0]

		self.nick="ChangeThis"
		self.ident="IrcBot"
		self.realname="Please read the examples."
		self.server=("irc.testnet.net", 6667)

		self.events={}

		self.add_event("state")
		self.add_event("raw")
		self.add_event("parsed")
		
		self.events['state'].add_listener(self.handle_state, 500)
		self.events['raw'].add_listener(self.handle_raw, 500)
		self.events['parsed'].add_listener(self.handle_parsed, 500)
		
	def main_loop(self):	
		if self.state==0:
			self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.set_state(1)
		if self.state > 1:
			self.send_and_recv()	
			self.process_readbuffer()
	def send_and_recv(self):
		if self.fd_status[1]==1 and len(self.sendbuffer)>0:
			n=self.socket.send(self.sendbuffer)
			if n==0:
				self.disconnect()
			self.sendbuffer=self.sendbuffer[n:]	
		if self.fd_status[0]==1:
			self.readbuffer=self.readbuffer+self.socket.recv(512)

	def process_readbuffer(self):
		parsed=string.split(self.readbuffer, "\n")
		self.readbuffer=parsed.pop()
		for line in parsed:
			if line[-1:]=='\r':
				line=line[:-1]
			self.events['raw'].call_listeners(line)

	def send_string(self, string):
		self.sendbuffer=self.sendbuffer+string+"\r\n"
	def set_state(self, newstate):
		self.state=newstate
		self.events['state'].call_listeners(newstate)
	def disconnect(self):
		try:
			self.socket.close()
		except error:
			pass
		self.readbuffer=""
		self.sendbuffer=""
		self.fd_status=[0, 0]
		self.set_state(-1)

	def handle_state(self, newstate):
		if newstate==1:
			self.socket.connect(self.server)
			self.set_state(2)
		elif newstate==2:
			self.send_string("NICK %s" % self.nick)
			self.send_string("USER %s %s :%s" % (self.ident, self.server, self.realname))
			self.set_state(3)
	def handle_raw(self, line):
		if line[0]==':':
			line=string.split(line, maxsplit=1)
			prefix=line[0][1:]
			line=string.join(line[1:])
		else:
			prefix=None
		line=string.split(line, maxsplit=1)
		command=line[0]
		line=string.join(line[1:])

		n=None
		for i in range(len(line)):
			if line[i]==':':
				if line[i-1]==' ' or i==0:
					n=i
					break
		if n==None:
			params=string.split(line)
		else:
			if n==0:
				params=[]
			else:
				params=string.split(line[:n-1])
			params.append(line[n+1:])	
		self.events['parsed'].call_listeners(prefix, command, params)
	def handle_parsed(self, prefix, command, params):
		if command=="PING":
			self.send_string("PONG :%s" % params[0])
		elif command=="001":
			self.set_state(4)

	def add_event(self, name, eventclass=None):
		if eventclass==None:
			eventclass=Simple_Event()
		self.events[name]=eventclass
		return eventclass
	def remove_event(self, name):
		del self.events[name]			
	
class Simple_Event:
	def __init__(self):
		self.listeners=[]
	def add_listener(self, function, prio=1000):
		self.listeners.append((prio, function))
		self.listeners.sort()
	def remove_listener(self, delfunction):
		for prio, function in listeners:
			if function==delfunction:
				del self.listeners[self.listeners.index((prio, function))]
	def call_listeners(self, *args):
		for prio, listener in self.listeners:
			listener(*args)
