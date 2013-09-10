"""
Program to generate simulated reverberation mapping data sets.
"""

import numpy as np
import numpy.random as rng
import matplotlib.pyplot as plt

def ar1(y0=0., mu=0., L=200., beta=1., n=1000):
	"""
	Simulate a time series from an AR(1) distribution.
	"""
	alpha = np.exp(-1./L)

	y = np.zeros(n)
	for i in xrange(1, n):
		y[i] = mu + alpha*(y[i-1] - mu) + beta*rng.randn()

	return y


if __name__ == '__main__':
	y = ar1()
	plt.plot(y)
	plt.show()

