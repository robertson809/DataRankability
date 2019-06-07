# TEST_RAND_PERT: Test the Spectral Rankability Measure on Randomly Perturbed Dominance Graph
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import specR
from random import sample
from copy import deepcopy
import matplotlib.pyplot as plt
import itertools
import numpy as np

### test variables
n = 50
kmax = n**2-n
itmax = 10
results = np.zeros(itmax)
rowcol = [x for x in itertools.product(range(n),range(n)) if x[0]!=x[1]]
spec = []

### perfect dominance graph adjacency
a = np.zeros((n,n))
for i in range(n):
    for j in range(i+1,n):
        a[i,j] = 1.

### main loop
for k in range(kmax+1):
    for it in range(itmax):
        # create k changes to dominance graph
        b = deepcopy(a)
        rsample = sample(rowcol,k)
        for i in range(k):
            b[rsample[i][0],rsample[i][1]] = 1 - b[rsample[i][0],rsample[i][1]] 
        # compute rankability
        results[it] = specR(b)
    # store averages
    spec.append(sum(results)/itmax)

### plot results
plt.plot(range(kmax+1),spec,label='specR')
plt.xlabel('Number of Changes')
plt.ylabel('Rankability')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
            ncol=1, mode="expand", borderaxespad=0.)
plt.show()