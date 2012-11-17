import sys
from averages import SimpleMovingAverage
import TradeRecord

class StrategyMan:

	def __init__(self):
		""" 
		Keeps track of the four strategies, detects crossovers, and logs trade records.

		Attributes:
			tick -- current "time", updated per point
			strategies -- dictionary of dictionaries for each strategy: sma, lwma, tma, ema and the 2 average types
			record -- a dictionary of records
		"""
		self.strategies = {'sma': {'slow': averages.SimpleMovingAverage(20), 'fast': averages.SimpleMovingAverage(5)}}

		self.HOST = 'localhost'
		self.PORT = 3001
 		
	def process(self, point):
		"""
		Updates the moving averages, sends the json to the GUI, then detects crossovers. 
		If necessary it performs the correct action to buy or sell, and if a trade
		occurs, it stores the record.

		Parameters:
			point -- the new price value to process
		"""
		self.tick+= 1
		for strat in strategies:
			strat['slow'].update(point)
			strat['fast'].update(point)

		action = detect_crossover(self.tick)

		if action == 0:
			# buy
		elif action == 1:
			# sell
		

	def detect_crossover(time):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
			-1 -- if no crossover
			0 -- if time to buy
			1 -- if time to sell
		"""



		return -1 # no crossover



	def buy(self):
 		self.send("B")

 		self.store_record(0, self.tick)

	def sell(self):
		self.send("S")

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

