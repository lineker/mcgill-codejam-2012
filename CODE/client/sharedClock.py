import sys
# new BuySellManager
class sharedClock:

	def __init__(self):
		self.clock = 0

	def add(self,n):
		self.clock = self.clock + n

	def get(self):
		return self.clock
