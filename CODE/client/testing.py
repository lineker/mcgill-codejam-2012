import sys
from averages import Simple, LinearWeighted, Triangular, Exponential
"""
This file contains a test for the averages formulas.
The output for each one of the strategies should be True.
The values on the lists below are the ones from the Proposal PDF at page 11
"""
price = [61.590,61.440,61.320,61.670,61.920,62.610,62.880,63.060,63.290,63.320,63.260,63.120,62.240,62.190,62.890]
sma = [61.59,61.515,61.45,61.505,61.588,61.792,62.08,62.428,62.752,63.032,63.162,63.21,63.046,62.826,62.74]
lwma = [61.59,61.49,61.405,61.511,61.647,61.988,62.351,62.677,62.965,63.154,63.23,63.216,62.893,62.607,62.629]
ema = [61.59,61.54,61.467,61.534,61.663,61.979,62.279,62.539,62.79,62.966,63.064,63.083,62.802,62.598,62.695]
tma = [61.59,61.553,61.518,61.515,61.53,61.57,61.683,61.879,62.128,62.417,62.691,62.917,63.04,63.055,62.997]

strategies = {'sma': {'slow': Simple(20), 'fast': Simple(5)}, 'lwma': {'slow': LinearWeighted(20), 'fast': LinearWeighted(5)}, 'ema': {'slow': Exponential(20), 'fast': Exponential(5)}, 'tma': {'slow': Triangular(20), 'fast': Triangular(5)}}

for i in range(0, 15):
	print "Price:"
	print price[i]
	for s in strategies:
		print ""
		print s
		updated = strategies[s]['fast'].update(price[i])
		if s == 'sma':
			print abs(sma[i] - updated) < 0.1
		elif s == 'lwma':
			print abs(lwma[i] - updated) < 0.1
		elif s == 'ema':
			print abs(ema[i] - updated) < 0.1
		elif s == 'tma':
			print abs(tma[i] - updated) < 0.1
	print ""
	print "-------------------------"
	print ""