#!/usr/bin/env python
import sys
from averages import Simple
from trade_record import TradeRecord

class StrategyMan:

	def __init__(self):
		""" 
		Keeps track of the four strategies, detects crossovers, and logs trade records.

		Attributes:
			tick -- current "time", updated per point
			strategies -- dictionary of dictionaries storing the strategys and their average objects for sma, lwma, tma, ema
			record -- a dictionary of records
			averages -- a dictionary of averages for the current tick in form
					{'sma': {'slow': val, 'fast': val2}, 'lwma' : {... }, ...}, 'tick2': ...} (same as strategies but with the actual values)
			hasBought -- flag indicating if a purchase has been made (if no purchase to date, cannot sell)

		"""
		self.strategies = {'sma': {'slow': Simple(20), 'fast': Simple(5)}}
		self.tick = 0
		self.HOST = 'localhost'
		self.PORT = 3001
		self.averages = {}
		self.hasBought = False
 		
	def process(self, point):
		"""
		Updates the moving averages, sends the json to the GUI, then detects crossovers. 
		If necessary it performs the correct action to buy or sell, and if a trade
		occurs, it stores the record.

		Parameters:
			point -- the new price value to process
		"""
		self.tick+= 1
		for strat in self.strategies:
			self.averages[strat]['slow'] = self.strategies[strat]['slow'].update(point)
			self.averages[strat]['fast'] = self.strategies[strat]['fast'].update(point)

		action = self.detect_crossover(self.tick)

		if action == 0:
			# buy
			self.buy()
			self.hasBought = True
			
		elif action == 1:
			# sell
			self.sell()
			self.hasBought = False
		

	def detect_crossover(self, time):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
			-1 -- if no crossover
			0 -- if time to buy
			1 -- if time to sell
		"""
		for strat in self.strategies:
			if self.averages[strat]['fast'] >= self.averages[strat]['slow'] && !self.hasBought:
				return 0
			elif self.averages[strat]['fast'] <= self.averages[strat]['slow'] && self.hasBought:
				return 1
			else:
				return -1 # no crossover



	def buy(self):
 		self.send("B\n")

 		self.store_record(0, self.tick)

	def sell(self):
		self.send("S\n")

		self.store_record(0, self.tick)

	def send(cmd):
		"""
		Sends the given command to the MS exchange using correct port and HOST

		Parameters:
			cmd -- the action type
		"""
		GET = '/rss.xml'

		try:
		  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(1)
		 
		try:
		  sock.connect((self.HOST, self.PORT))
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(2)

		sock.send(command + "\n")
		
		sock.close()

	def store_record(actionType, time):
		"""
		Store the action that took place at what time and get the manager
		Triggers the record to send itself to the Silanus API

		Parameters:
			actionType: 0 -- buy
			actionType: 1 -- sell
		"""

		manID # get the manager ID

		if actionType:
			# add the new trade to the record
			newRecord = TradeRecord(manID, "S", time)
		else:
			newRecord = TradeRecord(manID, "B", time)

		newRecord.send

