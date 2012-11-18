#!/usr/bin/env python
"""
Buy sell manager.
"""

import sys
from trade_record import TradeRecord
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


	def send(self, cmd, sType):
		"""
		Sends the given command to the MS exchange using correct port and HOST

		Parameters:
			cmd -- the action type
		"""
		self.sock.send(cmd + "\n")

	def terminate(self):
		self.sock.close()