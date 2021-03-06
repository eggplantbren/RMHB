from pylab import *

# Plot the posterior samples for a few objects

rc("font", size=16, family="serif", serif="Computer Sans")
rc("text", usetex=True)

bins = linspace(-4., 2., 101)

figure(figsize=(8, 9))

for i in xrange(0, 3):
	sample = loadtxt(str(i) + '.txt')
	subplot(3,1,i+1)
	hist(log10(sample[:,0]/10.), bins=bins, normed=True)
	xlim([-4, 2])
	gca().set_yticks([])

	if i < 2:
		gca().set_xticklabels([])
	else:
		xlabel(r'$\log_{10}(\bar{\tau}/(\textnormal{1 day}))$')

	if i==1:
		ylabel('Posterior Probability')

savefig('example_posteriors.pdf', bbox_inches='tight')
show()


