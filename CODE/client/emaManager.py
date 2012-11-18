#!/usr/bin/env python
import sys
from averages import Exponential
from trade_record import TradeRecord
import socket
from genericStrategyManager import GenericStrategyManager
import threading

class emaManager(GenericStrategyManager):

	def __init__(self, threadID, name, inq, clock, outq, transQ):
		super(threadID, name, inq, clock, outq, transQ)

		self.strategyType = 'ema'
		self.strategies['slow'] = Exponential(20)
		self.strategies['fast'] = Exponential(5)