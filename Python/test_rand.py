# TEST_RAND: Test the Spectral Rankability Measure on Perturbed Dominance Graph
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import specR, connR
from random import sample
from copy import deepcopy
import matplotlib.pyplot as plt
import itertools
import numpy as np


### test variables
n = 100
itmax = 10
kmax = n**2-n
results = np.zeros((itmax,2))
rowcol = [x for x in itertools.product(range(n),range(n)) if x[0]!=x[1]]
spec = []
conn = []

### perfect dominance graph adjacency
a = np.zeros((n,n))
for i in range(n):
    for j in range(i+1,n):
        a[i,j] = 1.

### main loop
for k in range(kmax):
    for it in range(itmax):
        # create k changes to dominance graph
        b = deepcopy(a)
        nk = 0
        rsample = sample(rowcol,k)
        for i in range(k):
            b[rsample[i][0],rsample[i][1]] = 1 - b[rsample[i][0],rsample[i][1]] 
        # compute rankability
        results[it,0] = specR(b)
        results[it,1] = connR(b)
    # store averages
    spec.append(sum(results[:,0])/itmax)
    conn.append(sum(results[:,1])/itmax)

### plot results
plt.plot(range(kmax),spec,label='specR')
plt.plot(range(kmax),conn,label='connR')
plt.xlabel('Number of Changes')
plt.ylabel('Rankability')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
            ncol=2, mode="expand", borderaxespad=0.)
plt.show()