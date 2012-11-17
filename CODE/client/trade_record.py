import sys
from json import dumps

class TradeRecord:

	def __init__(self, mid, action, time, strategyType, point):
		""" Attributes
		manager - the manager id for the trade
		action - a string "B":buy or "S":sell
		time - the time at which the action took place
		strategyType - the strategy type key
		"""
		self.price = point
		self.manager = mid
		self.action = action
		self.time = time
		self.strategyType = strategyType

	def send(self):
		"""
		sends the JSON form of itself to the Silanus API for signing by manager
		"""
		return dumps({
				"time": self.time,
				"type": self.strategyType,
				"price": self.price,
				"manager": self.manager,
				"strategy": self.strategyType})
 