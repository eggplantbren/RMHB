from pylab import *

def log_likelihood(params, xx):
	mu, sigma = params[0], params[1]
	logL = 0.
	for x in xx:
		f = 1./(sigma*sqrt(2.*pi))*exp(-0.5*((x - mu)/sigma)**2)
		logL += log(mean(f))
	return logL

# Load all of the posterior samples
xx = []
for i in xrange(0, 100):
	posterior_sample = loadtxt(str(i) + '.txt', usecols=[0])
	xx.append(log10(posterior_sample))

num = 512
mu = linspace(-3., 3., num)
sigma = linspace(0.05, 1., num)
[mu, sigma] = meshgrid(mu, sigma)
sigma = sigma[::-1, :]

logL = zeros(mu.shape)
for i in xrange(0, logL.shape[0]):
	for j in xrange(0, logL.shape[1]):
		logL[i, j] = log_likelihood([mu[i, j], sigma[i, j]], xx)
	print(i)

rc("font", size=16, family="serif", serif="Computer Sans")
rc("text", usetex=True)
imshow(exp(logL - logL.max()), aspect=6./0.99, extent=[-3, 3, 0.05, 1])
plot(1.867, 0.157, 'wo')
xlabel('$\\mu$')
ylabel('$\\sigma$')
savefig('posterior.eps', bbox_inches='tight')
show()

