#!/usr/bin/env python
import sys
from averages import Triangular
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class tmaManager(GenericStrategyMan):

	def __init__(self, threadID, name, inq, clock, outq, transQ, port):
		super(tmaManager, self).__init__(threadID, name, inq, clock, outq, transQ, port)

		self.strategyType = 'tma'
		self.strategies['slow'] = Triangular(20)
		self.strategies['fast'] = Triangular(5)
