from pylab import *

data1 = loadtxt('../../models/ts_simulations/objects/sim001.txt')
data2 = loadtxt('../../models/ts_simulations/objects/sim001_line.txt')

data1[:,0] *= 10
data2[:,0] *= 10
savetxt('data1.txt', data1)
savetxt('data2.txt', data2)

