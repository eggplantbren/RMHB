from pylab import *

def simulate_data(which=0, numpoints=5):

	lags = []
	weights = []

	for k in xrange(0, 100):
		# Make the first time series
		L = exp(log(100.) + log(100.)*rand())
		alpha = exp(-1./L)
		beta = exp(log(0.2) + log(5.)*rand())

		y1 = zeros(1000)
		for i in xrange(1, 1000):
			y1[i] = alpha*y1[i-1] + beta*randn()
		y1 += 50.

		# Make the second time series
		b = exp(log(100.) + 0.3*randn())
		a = rand()*b
		tau = (a + b)/2.
		if b >= 500.:
			print('WARNING!')

		y2 = zeros(1000)
		for i in xrange(500, 1000):
			y2[i] = mean(y1[(i-b):(i-a+1)])
		y2 *= 0.5

		# Make datasets
		which1 = sort(randint(1000, size=100))
		which2 = 500 + sort(randint(500, size=numpoints))

		sigma1, sigma2 = 1., 0.25
		data1 = zeros((100, 3))
		data2 = zeros((numpoints, 3))
		data1[:,0] = which1
		data1[:,1] = y1[which1] + sigma1*randn(100)
		data1[:,2] = sigma1

		data2[:,0] = which2
		data2[:,1] = y2[which2] + sigma2*randn(numpoints)
		data2[:,2] = sigma2

		if k == which:
			savetxt('data1.txt', data1)
			savetxt('data2.txt', data2)

		for ii in xrange(0, data1.shape[0]):
			for jj in xrange(0, data2.shape[0]):
				lags.append(data2[jj, 0] - data1[ii, 0])
				weights.append((data1[ii, 1] - mean(data1[:,1]))*(data2[jj, 1] - mean(data2[:,1])))

	lags = array(lags)
	weights = array(weights)

#	rc("font", size=16, family="serif", serif="Computer Sans")
#	rc("text", usetex=True)


#	hist(lags[abs(lags - 150) < 150], 300, weights=weights[abs(lags - 150) < 150], alpha=0.25)
#	xlim([0, 300])
#	ylim(-50)
#	xlabel('Lag $\\tau$')
#	ylabel('Stacked Cross-Correlation Function')
#	savefig('ccf.pdf')
#	show()

import os
seed(123)
import postprocess

for i in xrange(0, 100):
	simulate_data(i, numpoints=2)

	f = open('OPTIONS_TEMPLATE', 'r')
	o = f.read()
	f.close()

	o = o.replace('XXX', '500')
	o = o.replace('YYY', '500')
	f = open('OPTIONS', 'w')
	f.write(o)
	f.close()

	os.system('./main -t 8')
		
	l = loadtxt('levels.txt')
	l = l[l[:,1] <= -30., :]

	f = open('OPTIONS_TEMPLATE', 'r')
	o = f.read()
	f.close()

	o = o.replace('XXX', str(l.shape[0]))
	o = o.replace('YYY', '3000')
	f = open('OPTIONS', 'w')
	f.write(o)
	f.close()

	os.system('./main -t 8')
	postprocess.postprocess(cut=0.3333, plot=False)
	os.system('cp posterior_sample.txt Results/' + str(i) + '.txt')

