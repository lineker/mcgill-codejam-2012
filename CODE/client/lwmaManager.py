#!/usr/bin/env python
import sys
from averages import LinearWeighted
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class lwmaManager(GenericStrategyMan):

	def __init__(self, threadID, name, inq, clock, outq, transQ, port):
		super(lwmaManager, self).__init__(threadID, name, inq, clock, outq, transQ, port)

		self.strategyType = 'lwma'
		self.strategies['slow'] = LinearWeighted(20)
		self.strategies['fast'] = LinearWeighted(5)
