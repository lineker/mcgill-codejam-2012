#!/usr/bin/env python
"""
Buy sell manager.
"""

import sys

import socket

# new BuySellManager
class BuySellManager:

	def __init__(self):

		self.HOST = 'localhost'
		self.PORT = 3001

		try:
		  self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(1)
		
		try:
		  self.sock.connect((self.HOST, self.PORT))
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(2)


	def send(self, cmd, sType, transactions, manager, time, web_sock):
		"""
		Sends the given command to the MS exchange using correct port and HOST

		Parameters:
			cmd -- the action type
		"""
		self.sock.send(cmd + "\n")
		try:
			response = self.sock.recv(100)
			#check if is a ERROR , maybe market is already closed
			if(str(response).rfind("E") != -1):
				print "market ERROR"
			else:
				#create transaction
				print "resp for "+sType+" cmd : "+response
				#transactions[sType].put([time,cmd,float(response),manager,sType])
				web_sock.send("T|"+str(time)+"|"+str(cmd)+"|"+str(response.strip())+"|"+str(manager)+"|"+str(sType)+"\n")
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		
		

	def terminate(self):
		self.sock.close()

