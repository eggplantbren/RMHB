from pylab import *

seed(123)

# Make the first time series
y1 = zeros(1000)
for i in xrange(1, 1000):
	y1[i] = 0.99*y1[i-1] + 1.*randn()
y1 += 50.

# Make the second time series
a = 50
b = 100
y2 = zeros(1000)
for i in xrange(500, 1000):
	y2[i] = mean(y1[(i-b):(i-a)])
y2 *= 0.5

# Make datasets
which1 = sort(randint(1000, size=100))
which2 = 500 + sort(randint(500, size=100))

sigma = 1.
data1 = zeros((100, 3))
data2 = zeros((100, 3))
data1[:,0] = which1
data1[:,1] = y1[which1] + sigma*randn(100)
data1[:,2] = sigma

data2[:,0] = which2
data2[:,1] = y2[which2] + sigma*randn(100)
data2[:,2] = sigma

data2 = data2[array([20, 60, 80]), :]

savetxt('data1.txt', data1)
savetxt('data2.txt', data2)

plot(y1, 'b')
plot(y2, 'r')
errorbar(data1[:,0], data1[:,1], yerr=data1[:,2], fmt='bo')
errorbar(data2[:,0], data2[:,1], yerr=data2[:,2], fmt='ro')
show()

