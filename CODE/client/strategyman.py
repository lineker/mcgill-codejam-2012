import sys
from averages import SimpleMovingAverage

class StrategyMan:

	def __init__(self):

		""" Attributes:
		tick - updated per point
		strategies - dictionary of dictionaries for each strategy: sma, lwma, tma, ema and the 2 average types
		record - a dictionary of records
		
		"""
		self.strategies = {'sma': {'slow': averages.SimpleMovingAverage(20), 'fast': averages.SimpleMovingAverage(5)}}

		self.HOST = 'localhost'
		self.PORT = 3001
 		
	def update(self, point):
		"""
		Updates the moving averages, sends the json to the GUI, then detects crossovers. 
		If necessary it performs the correct action to buy or sell, and if a trade
		occurs, it stores the record.
		"""
		self.tick+= 1
		for strat in strategies: 
			strat['slow'].update(point)
			strat['fast'].update(point)


 	def buy(self):
 		self.send("B")

 		self.store_record(0, )

	def sell(self):
		self.send("S")

	def send(cmd):
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

	def store_record(actionType):
		"""
		Store the action that took place at what time and get the manager
		actionType 0 - buy
		actionType 1 - sell
		"""

		if actionType:

		else:



