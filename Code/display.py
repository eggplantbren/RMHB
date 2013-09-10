import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt('data1.txt')
data2 = np.loadtxt('data2.txt')
posterior_sample = np.atleast_2d(np.loadtxt('posterior_sample.txt'))

points = 1500

plt.ion()
for i in xrange(0, posterior_sample.shape[0]):
	plt.hold(False)
	plt.errorbar(data1[:,0], data1[:,1], yerr=data1[:,2], fmt='ko')
	plt.hold(True)
	plt.plot(posterior_sample[i, 8:8+points], 'b', linewidth=2, alpha=0.5)
	plt.errorbar(data2[:,0], data2[:,1], yerr=data2[:,2], fmt='go')
	plt.plot(data2[:,0], posterior_sample[i, 8+points:], 'c', linewidth=2, alpha=0.5)
	plt.xlabel('Time', fontsize=16)
	plt.ylabel('$y$', fontsize=16)
	plt.title((i+1))
	plt.xlim([-0.5, 1000.5])
	plt.ylim([-30., 100.])
	plt.draw()

plt.ioff()
plt.show()

