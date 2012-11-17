#!/usr/bin/env python
import sys
from averages import Simple, LinearWeighted, Triangular, Exponential
from trade_record import TradeRecord
import socket


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
			mSchedule -- manager schedule to get the manager for sending records. To understand how it works, ask Rebecca.
			sock -- the socket connection to the MS Exchange on port 3001 for making trades
			trend -- the current trend of the averages 
				0 -- starting default
				-1 -- fast is on bottom, slow on top (watch for upward trend)
				1 -- slow on bottom, fast on top (watch for downward trend)
		"""

		self.strategies = {'sma': {'slow': Simple(20), 'fast': Simple(5)}, 'lwma': {'slow': LinearWeighted(20), 'fast': LinearWeighted(5)}, 'ema': {'slow': Exponential(20), 'fast': Exponential(5)}, 'tma': {'slow': Triangular(20), 'fast': Triangular(5)}}
		self.tick = 0
		self.HOST = 'localhost'
		self.PORT = 3001
		self.averages = {'sma': {'slow': None, 'fast': None}, 'tma': {'slow': None, 'fast': None}, 'lwma': {'slow': None, 'fast': None}, 'ema': {'slow': None, 'fast': None}}
		self.trend = {'sma': 0, 'lwma': 0, 'ema': 0, 'tma': 0}

		self.mSchedule = [[1, 2, 1, 2], [3, 4, 3, 4], [1, 2, 1, 2], [1, 2, 1, 2], [3, 4, 3, 4], [3, 4, 3, 4], [5, 6, 5, 6], [7, 8, 7, 8]]


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

		result = self.detect_crossover(self.tick)
		
		if result:
			if result['action'] == 0:
				# buy
				self.buy()
				self.store_record(0, self.tick, result['sType'])
				
			elif result['action'] == 1:
				# sell
				self.sell()
				self.store_record(1, self.tick, result['sType'])	

		# send data to GUI


	def detect_crossover(self, time):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
			-1 -- if no crossover
			0 -- if time to buy
			1 -- if time to sell
			and the strategy type of the strategy which had the crossover.
		"""


		for strat in self.strategies:
					# when time = 0 set trend
			if self.trend[strat] == 0:
				if self.averages[strat]['fast'] > self.averages[strat]['slow']:
					self.trend[strat] = -1
				elif self.averages[strat]['fast'] < self.averages[strat]['slow']:
					self.trend[strat] = 1
				else:
					self.trend[strat] = 0
			else: 
				if self.trend[strat]== -1 and self.averages[strat]['fast'] >= self.averages[strat]['slow']:
					self.trend[strat] = 1
					return {'action': 0, 'sType': strat}
				elif self.trend[strat]== 1 and self.averages[strat]['fast'] <= self.averages[strat]['slow']:
					self.trend[strat] = -1
					return {'action': 1, 'sType': strat}
				else:
					return None # no crossover


	def buy(self):
 		self.send("B\n")
 		print "Buying something\n"

	def sell(self):
		self.send("S\n")
		print  "Selling something\n"

	def send(self, cmd):
		"""
		Sends the given command to the MS exchange using correct port and HOST

		Parameters:
			cmd -- the action type
		"""
		self.sock.send(cmd + "\n")


	def store_record(self, actionType, time, strategyType):
		"""
		Store the action that took place at what time and get the manager
		Triggers the record to send itself to the Silanus API

		Parameters:
			actionType: 0 -- buy
			actionType: 1 -- sell
		"""

		manID = self.getManager(time, strategyType)
	
		if actionType:
			# add the new trade to the record
			newRecord = TradeRecord(manID, "S", time, strategyType)
		else:
			newRecord = TradeRecord(manID, "B", time, strategyType)

		newRecord.send()

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






