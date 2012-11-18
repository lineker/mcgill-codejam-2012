#!/usr/bin/env python
import sys
from average import Simple
from trade_record import TradeRecord
import socket
from genericStrategyManager import GenericStrategyManager


class smaManager(GenericStrategyManager):

	def __init__(self):
		super()

		self.strategyType = 'sma'
		self.strategies['slow'] = Simple(20)
		self.strategies['fast'] = Simple(5)
		self.PORT = 3001
