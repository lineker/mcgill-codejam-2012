#!/usr/bin/env python
"""
Interface for all strategy managers, containing data structures and necessary methods.
Keeps track of the four strategies, detects crossovers, and logs trade records.
"""

import sys
import socket
import threading
import Queue
from buySellManager import BuySellManager

# new BuySellManager
HOST = "localhost"

class GenericStrategyMan( threading.Thread ):

	def __init__(self, threadID, name, inq, clock, outq, transQ):

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
		threading.Thread.__init__(self)
		self.tQueue = transQ
		self.threadID = threadID
		self.name = name
		self.inputQueue = inq
		self.outputQueue = outq
		self.strategies = {'slow': None, 'fast': None }
		self.tick = clock
		self.HOST = 'localhost'
		self.exitFlag = False
		self.bsManager = BuySellManager()

		try:
		  self.web_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		  pass
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(1)
		 
		try:
		  self.web_soc.connect((HOST, self.PORT))
		  pass
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(2)

		""" 
			PORTS:
			sma at 9001
			lwma at 9002
			ema at 9003
			tma at 9004
		"""
		self.averages = {'slow': None, 'fast': None}
		self.trend = 0
		self.mSchedule = [[1, 2, 1, 2], [3, 4, 3, 4], [1, 2, 1, 2], [1, 2, 1, 2], [3, 4, 3, 4], [3, 4, 3, 4], [5, 6, 5, 6], [7, 8, 7, 8]]
		self.transactions = []


	def run(self):
		print "Starting " + self.strategyType
		while not self.exitFlag:
	        	if not self.inputQueue.empty():
	            		data = self.inputQueue.get()
	            		self.tick += 1 
	            		self.process(data)
	  

	def process(self, point):
		"""
		Updates the moving averages, sends the json to the GUI, then detects crossovers. 
		If necessary it performs the correct action to buy or sell, and if a trade
		occurs, it stores the record.

		Parameters:
			point -- the new price value to process
		"""
		print "Processing "+str(point)+" at " + self.strategyType
		
		
		self.averages['slow'] = self.strategies['slow'].update(point)
		self.averages['fast'] = self.strategies['fast'].update(point)

		# output point and the two averages
		self.web_soc.send("A|"+str(point)+"|"+str(self.averages['slow'])+"|"+self.averages['fast']+"\n")
		#self.outputQueue.put({'price': point, 'slowAvg': self.averages['slow'], 'fastAvg': self.averages['fast'], 'time':self.tick})

		result = self.detect_crossover()

		if result:
			if result['action'] == 0:
				# buy
				self.buy()
				
			elif result['action'] == 1:
				# sell
				self.sell()			

	def detect_crossover(self):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
			-1 -- if no crossover
			0 -- if time to buy
			1 -- if time to sell
			and the strategy type of the strategy which had the crossover.
		"""

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
		#cmd, sType, transactions, manager, time)
 		self.bsManager.send("B", self.strategyType, self.tQueue, self.getManager(self.strategyType), self.tick, self.web_soc)

	def sell(self):
		self.bsManager.send("S", self.strategyType,self.tQueue, self.getManager(self.strategyType), self.tick, self.web_soc)

	def getManager(self, sType):
		"""
		Returns the manager supervising the given strategy at a given time.
		Parameters:
			time -- the time at which the trade was made
			strategyType -- the strategy type of the trade
		Returns:
			id -- manager id
		"""

		strategyType = 0
		time = self.tick + 32400
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

