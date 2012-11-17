import sys
from json import dumps

class TradeRecord:

	def __init__(self, id, action, time):
		""" Attributes
		manager - the manager id for the trade
		action - a string "B":buy or "S":sell
		time - the time at which the action took place
		"""

	def send(self):
		"""
		sends the JSON form of itself to the Silanus API for signing by manager
		"""
