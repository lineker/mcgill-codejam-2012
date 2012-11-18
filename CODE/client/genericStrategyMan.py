#!/usr/bin/env python
"""
Interface for all strategy managers, containing data structures and necessary methods.
Keeps track of the four strategies, detects crossovers, and logs trade records.
"""

import sys
from trade_record import TradeRecord
import socket



class GenericStrategyMan:

	def __init__(self):
		""" 
		Attributes:
			tick -- current "time", updated per point
			strategies -- dictionary of dictionaries storing the strategys and their average objects for sma, lwma, tma, ema
			record -- a dictionary of records
			averages -- a dictionary of averages for the current tick in form
					{'sma': {'slow': val, 'fast': val2}, 'lwma' : {... }, ...}, 'tick2': ...} (same as strategies but with the actual values)
			hasBought -- flag indicating if a purchase has been made (if no purchase to date, cannot sell)
			mSchedule -- manager schedule to get the manager for sending records. To understand how it works, ask Rebecca.
			sock -- the socket connection to the MS Exchange on specified port for making trades
			trend -- the current trend of the averages
				0 -- starting default
				-1 -- fast is on bottom, slow on top (watch for upward trend)
				1 -- slow on bottom, fast on top (watch for downward trend)
			transactions -- array of trade records
		"""
		self.strategyType = ""
		self.strategies = {'slow': None, 'fast': None }
		self.tick = 0
		self.HOST = 'localhost'
		self.PORT = 0
		""" 
		PORTS:
			sma at 3001
			lwma at 3002
			ema at 3003
			tma at 3004
		"""
		self.averages = {'slow': None, 'fast': None}
		self.trend = 0
		self.mSchedule = [[1, 2, 1, 2], [3, 4, 3, 4], [1, 2, 1, 2], [1, 2, 1, 2], [3, 4, 3, 4], [3, 4, 3, 4], [5, 6, 5, 6], [7, 8, 7, 8]]
		self.transactions = []

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

 		
	def process(self, point, time):
		"""
		Updates the moving averages, sends the json to the GUI, then detects crossovers. 
		If necessary it performs the correct action to buy or sell, and if a trade
		occurs, it stores the record.

		Parameters:
			point -- the new price value to process
		"""
		self.tick = time
		
		self.averages['slow'] = self.strategies['slow'].update(point)
		self.averages['fast'] = self.strategies['fast'].update(point)

		result = self.detect_crossover(self.tick)
		
		if result:
			if result['action'] == 0:
				# buy
				self.buy()
				self.store_record(0, self.tick, self.strategyType, point)
				
			elif result['action'] == 1:
				# sell
				self.sell()
				self.store_record(1, self.tick, self.strategyType, point)

		# send data to GUI here!


	def detect_crossover(self, time):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
			-1 -- if no crossover
			0 -- if time to buy
			1 -- if time to sell
			and the strategy type of the strategy which had the crossover.
		"""


				# when time = 0 set trend
		if self.trend == 0:
			if self.averages['fast'] > self.averages['slow']:
				self.trend = -1
			elif self.averages['fast'] < self.averages['slow']:
				self.trend = 1
			else:
				self.trend = 0
		else: 
			if self.trend == -1 and self.averages['fast'] >= self.averages['slow']:
				self.trend = 1
				return {'action': 0, 'sType': self.strategyType}
			elif self.trend == 1 and self.averages['fast'] <= self.averages['slow']:
				self.trend = -1
				return {'action': 1, 'sType': self.strategyType}
			else:
				return None # no crossover


	def buy(self):
 		self.send("B\n")
 		print "Buying something from " + self.strategyType + "\n"

	def sell(self):
		self.send("S\n")
		print  "Selling something " + self.strategyType + "\n"

	def send(self, cmd):
		"""
		Sends the given command to the MS exchange using correct port and HOST

		Parameters:
			cmd -- the action type
		"""
		self.sock.send(cmd + "\n")


	def store_record(self, actionType, time, point):
		"""
		Store the action that took place at what time and get the manager
		Triggers the record to send itself to the Silanus API

		Parameters:
			actionType: 0 -- buy
			actionType: 1 -- sell
		"""

		manID = self.getManager(time, self.strategyType)
	
		if actionType:
			# add the new trade to the record
			newRecord = TradeRecord(manID, "S", time, self.strategyType, point)
		else:
			newRecord = TradeRecord(manID, "B", time, self.strategyType, point)

		newRecord.send()
		self.transactions.append(newRecord)

	def getManager(self, tick, sType):
		"""
		Returns the manager supervising the given strategy at a given time.
		Parameters:
			time -- the time at which the trade was made
			strategyType -- the strategy type of the trade
		Returns:
			id -- manager id
		"""

		strategyType = 0
		time = tick + 32400
		if sType == 'sma':
			strategyType = 0
		elif sType == 'lwma':
			strategyType = 1
		elif sType == 'ema':
			strategyType = 2
		else:
			strategyType = 3 #tma


		if time <= 39600:
			return self.mSchedule[1][strategyType]
		elif time <= 41400:
			return self.mSchedule[2][strategyType]
		elif time <= 46800:
			return self.mSchedule[3][strategyType]
		elif time <= 48600:
			return self.mSchedule[4][strategyType]
		elif time <= 55800:
			return self.mSchedule[5][strategyType]
		elif time <= 63000:
			return self.mSchedule[6][strategyType]
		else:
			return self.mSchedule[7][strategyType]

	def getTransactions(self):
		return self.transactions

	def getAverages(self):
		return self.averages

