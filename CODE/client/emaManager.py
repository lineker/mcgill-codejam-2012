#!/usr/bin/env python
import sys
from averages import Exponential
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class emaManager(GenericStrategyMan):
	PORT = 9003
	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(emaManager, self).__init__(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'ema'
		self.strategies['slow'] = Exponential(20)
		self.strategies['fast'] = Exponential(5)
