#!/usr/bin/env python
import sys
from averages import LinearWeighted
from trade_record import TradeRecord
import socket
from genericStrategyManager import GenericStrategyManager
import threading

class lwmaManager(GenericStrategyManager):

	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'lwma'
		self.strategies['slow'] = LinearWeighted(20)
		self.strategies['fast'] = LinearWeighted(5)
