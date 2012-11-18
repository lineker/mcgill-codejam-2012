#!/usr/bin/env python
import sys
from averages import Triangular
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class tmaManager(GenericStrategyMan):
	PORT = 9004
	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(tmaManager, self).__init__(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'tma'
		self.strategies['slow'] = Triangular(20)
		self.strategies['fast'] = Triangular(5)
