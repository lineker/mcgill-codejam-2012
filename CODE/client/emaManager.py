#!/usr/bin/env python
import sys
from averages import Exponential
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class emaManager(GenericStrategyMan):

	def __init__(self, threadID, name, inq, clock, outq, transQ, port):
		super(emaManager, self).__init__(threadID, name, inq, clock, outq, transQ, port)

		self.strategyType = 'ema'
		self.strategies['slow'] = Exponential(20)
		self.strategies['fast'] = Exponential(5)
