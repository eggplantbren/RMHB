from pylab import *

seed(123)
which = 0

for k in xrange(0, 100):
	# Make the first time series
	L = exp(log(100.) + log(100.)*rand())
	alpha = exp(-1./L)
	beta = exp(log(0.05) + log(20.)*rand())

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
	which2 = 500 + sort(randint(500, size=2))

	sigma1, sigma2 = 1., 1.
	data1 = zeros((100, 3))
	data2 = zeros((2, 3))
	data1[:,0] = which1
	data1[:,1] = y1[which1] + sigma1*randn(100)
	data1[:,2] = sigma1

	data2[:,0] = which2
	data2[:,1] = y2[which2] + sigma2*randn(2)
	data2[:,2] = sigma2

	if k == which:
		savetxt('data1.txt', data1)
		savetxt('data2.txt', data2)

		plot(y1, 'b')
		plot(y2, 'r')
		errorbar(data1[:,0], data1[:,1], yerr=data1[:,2], fmt='bo')
		errorbar(data2[:,0], data2[:,1], yerr=data2[:,2], fmt='ro')
		show()

