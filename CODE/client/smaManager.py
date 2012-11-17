#!/usr/bin/env python
import sys
from averages import Simple
from trade_record import TradeRecord
import socket
from genericStrategyMan import GenericStrategyMan
import threading

class smaManager(GenericStrategyMan):

	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'sma'
		self.strategies['slow'] = Simple(20)
		self.strategies['fast'] = Simple(5)
