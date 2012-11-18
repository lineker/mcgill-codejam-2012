#!/usr/bin/env python
import sys
from averages import Simple
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class smaManager(GenericStrategyMan):

	def __init__(self, threadID, name, inq, clock, outq, transQ, port):
		super(smaManager, self).__init__(threadID, name, inq, clock, outq, transQ, port)

		self.strategyType = 'sma'
		self.strategies['slow'] = Simple(20)
		self.strategies['fast'] = Simple(5)
