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

post = exp(logL - logL.max())
post = post/post.sum()
imshow(post, aspect=6./0.99, extent=[-3, 3, 0.05, 1])
hold(True)
plot(1.867, 0.157, 'w*', markersize=10)
ylim(0.05)
xlabel('$\\mu$')
ylabel('$\\sigma$')
savefig('posterior.pdf', bbox_inches='tight')
show()

figure(figsize=(10, 8))
# Compute marginal posterior for mu
# and predictive distribution for a new tau
p = post.sum(axis=0)
p /= trapz(p, x=mu[0, :])
plot(mu[0, :], p, 'b', linewidth=2, label='Posterior distribution for $\\mu$')

predictive = zeros(mu[0, :].shape)
for i in xrange(0, post.shape[0]):
	for j in xrange(0, post.shape[1]):
		predictive += post[i, j]/(sigma[i, j]*sqrt(2.*pi))*exp(-0.5*((mu[0, :] - mu[i, j])/sigma[i, j])**2)

plot(mu[0, :], predictive, 'r--', linewidth=2, label='Predictive distribution for new $\\bar{\\tau}$')
xlim([0, 3])
legend(loc = 'upper left')
ylabel('Probability Density', fontsize=18)
xlabel('$\\mu$,  log$_{10}(\\bar{\\tau})$', fontsize=20)
savefig('posterior2.pdf', bbox_inches='tight')
show()

