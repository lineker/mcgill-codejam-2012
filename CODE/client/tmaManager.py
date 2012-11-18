#!/usr/bin/env python
import sys
from averages import Triangular
from trade_record import TradeRecord
import socket
from genericStrategyManager import GenericStrategyManager
import threading

class tmaManager(GenericStrategyManager):

	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'tma'
		self.strategies['slow'] = Triangular(20)
		self.strategies['fast'] = Triangular(5)