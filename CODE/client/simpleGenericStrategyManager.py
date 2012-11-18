
import time

class simpleGenericStrategyManager(object):

	def __init__(self,tchan):
		self.strategies = {'slow': None, 'fast': None }
		self.averages = {'slow': None, 'fast': None}
		self.trend = 0
		self.t_ch = tchan

	def timing(f):
		def wrap(*args):

			time1 = time.time()
			ret = f(*args)
			time2 = time.time()
			print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
			return ret
		return wrap

	#@timing
	def process(self, point):
		#print "process " + self.strategyType
		self.averages['slow'] = self.strategies['slow'].update(point)
		self.averages['fast'] = self.strategies['fast'].update(point)
		
		slowAvg = self.averages['slow']
		fastAvg = self.averages['fast']
		#print "slow " + self.strategyType
		#print slowAvg
		result = self.detect_crossover()

		if result:
			if result['action'] == 0:
				#print "buy"
				# buy
				#self.buy()
				self.t_ch.send(['T','B',self.strategyType, point])
			elif result['action'] == 1:
				#print "sell"
				# sell
				#self.sell()
				self.t_ch.send(['T','S',self.strategyType, point])
			else:
				self.t_ch.send(['A',point,slowAvg,fastAvg,self.strategyType])
		else:
			self.t_ch.send(['A',point,slowAvg,fastAvg,self.strategyType])

	def detect_crossover(self):
		"""
		Detects a crossover between the slow and fast moving averages for each strategy.
		Returns:
		-1 -- if no crossover
		0 -- if time to buy
		1 -- if time to sell
		and the strategy type of the strategy which had the crossover."""
	

		if self.trend == 0:
			if self.averages['fast'] < self.averages['slow']:
				self.trend = -1
			elif self.averages['fast'] >= self.averages['slow']:
				self.trend = 1
		else: 
			if self.trend == -1 and self.averages['fast'] >= self.averages['slow']:
				self.trend = 1
				return {'action': 0, 'sType': self.strategyType}
			elif self.trend == 1 and self.averages['fast'] <= self.averages['slow']:
				self.trend = -1
				return {'action': 1, 'sType': self.strategyType}
			else:
				return None # no crossover


from averages import Simple,Exponential,Triangular,LinearWeighted

class simpleEmaManager(simpleGenericStrategyManager):
	def __init__(self,param):
		super(simpleEmaManager, self).__init__(param)
		self.strategyType = 'ema'
		self.strategies['slow'] = Exponential(20)
		self.strategies['fast'] = Exponential(5)


class simpleTmaManager(simpleGenericStrategyManager):
	def __init__(self,param):
		super(simpleTmaManager, self).__init__(param)

		self.strategyType = 'tma'
		self.strategies['slow'] = Triangular(20)
		self.strategies['fast'] = Triangular(5)

class simpleSmaManager(simpleGenericStrategyManager):
	def __init__(self,param):
		super(simpleSmaManager, self).__init__(param)

		self.strategyType = 'sma'
		self.strategies['slow'] = Simple(20)
		self.strategies['fast'] = Simple(5)

class simpleLwmaManager(simpleGenericStrategyManager):
	def __init__(self,param):
		super(simpleLwmaManager, self).__init__(param)

		self.strategyType = 'lwma'
		self.strategies['slow'] = LinearWeighted(20)
		self.strategies['fast'] = LinearWeighted(5)