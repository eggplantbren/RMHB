from pylab import *

rc("font", size=16, family="serif", serif="Computer Sans")
rc("text", usetex=True)

def ccf(data1, data2, log10_tau, delta=0.1):
	"""
	Get the cross-correlation between log10_tau and log10_tau + delta
	"""
	s = 0.
	c_bar = data1[:,1].mean()

	nl = data2.shape[0]

	# Loop over line measurements
	for j in xrange(0, nl):
		# Calculate mean line flux, excluding current point
		which = ones(nl)
		which[j] = 0.
		which = which.astype('bool')
		l_bar = data2[which,1].mean()

		# Time difference between all continuum measurements
		dd = data2[j,0] - data1[:,0]

		# Find those within the bin
		include = nonzero(logical_and(dd >= 10.**log10_tau,
					dd < 10.**(log10_tau + delta)))[0]

		if len(include) >= 1:
			for ii in include:
				s += ((nl - 1.)/nl*(data1[ii, 1] - c_bar)*
						(data2[j, 1] - l_bar))/len(include)
	return s



def simulate_data(which=0, numpoints=5):
#	log10_tau = linspace(-3, 3, 301)
#	sccf = zeros(log10_tau.size)

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

#		temp = zeros(log10_tau.size)
#		for ii in xrange(0, log10_tau.size):
#			temp[ii] = ccf(data1, data2, log10_tau[ii],
#					delta=log10_tau[1] - log10_tau[0])
#		sccf += temp

#		if k==99:
#			bar(log10_tau - 1., sccf, width=log10_tau[1] - log10_tau[0],
#						alpha=0.2)
#			xlabel(r'$\log_{10}(\tau/(\textnormal{1 day}))$')
#			ylabel('Stacked CCF')
#			xlim([0, 2])
#			axhline(0, color='k')
#			savefig('ccf.pdf', bbox_inches='tight')
#			show()

#		if k==0:
#			figure(figsize=(8, 9))
#		if k < 3:
#			subplot(3, 1, k+1)
#			errorbar(data1[:,0]/10, data1[:,1], yerr=data1[:,2], fmt='bo', markersize=3, label='Continuum')
#			errorbar(data2[:,0]/10, data2[:,1], yerr=data2[:,2], fmt='r*', markersize=5, label='Line')
#			gca().set_yticks([0, 20, 40, 60])

#			if k == 1:
#				ylabel('Flux')
#			if k < 2:
#				gca().set_xticks([])
#			else:
#				xlabel('Time (days)')
#				legend(loc='lower left', numpoints=1)
#				savefig('data.pdf', bbox_inches='tight')
#				show()

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

