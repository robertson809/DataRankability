# RM: Rankability Measure
#
# This module contains the functions for Hillside Rankability measure and Spectral Rankability measure.
#
# Author: Thomas R. Cameron
# Date: 10/13/2019
import itertools
from math import factorial
import numpy as np
import pulp

TOL = np.finfo(float).eps

###############################################
###             Hausdorff                   ###
###############################################
#   Hausdorff distance between sets e and s.
###############################################
def Hausdorff(e,s):
    """Hausdorff distance between sets e and s."""
    def _sv(e,s):
        return max([min([abs(e[i]-s[j]) for j in range(len(s))]) for i in range(len(e))])
    return max(_sv(e,s),_sv(s,e))
###############################################
###             specR                       ###
###############################################
#   Computes Spectral Rankability Measure.
###############################################
def specR(a):
    """Computes Spectral Rankability Measure."""
    # given graph Laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # perfect dominance graph spectrum and out-degree
    s = np.array([n-k for k in range(1,n+1)])
    # eigenvalues of given graph Laplacian
    e = np.linalg.eigvals(l)
    # rankability measure
    return 1. - ((Hausdorff(e,s)+Hausdorff(x,s))/(2*(n-1)))
###############################################
###             hillR_BF                    ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
def hillR_BF(a):
    """Computes Hillside Rankability Measure using brute force method."""
    # build c matrix from data matrix a 
    n = len(a)
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = -(np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int)))
    # compute kstar, kworst, and p using brute force method
    fitness = []
    perm = list(itertools.permutations(range(n)))
    for k in range(len(perm)):
        temp = c[perm[k],:]
        temp = temp[:,perm[k]]
        temp = temp*np.triu(np.ones((n,n)))
        fitness.append(-np.sum(temp))
    kstar=np.amin(fitness);
    kworst=np.amax(fitness);
    #p = sum((fitness==kstar).astype(int))
    # compute rankability
    if(kstar==0 and kworst==0):
        return 0.
    else:
        #return 1. - kstar*p/(kworst*factorial(n))
        return (kworst-kstar)/(kworst+kstar)
###############################################
###             hillR_LP                    ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
def hillR_LP(a):
    """Computes Hillside Rankability Measure by solving LP using Pulp."""
    # build c matrix from data matrix a 
    n = len(a)
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int))
    # hillside rankability pulp class
    hillLP= pulp.LpProblem("Hillside LP",pulp.LpMinimize)
    # decision variables
    x = [[pulp.LpVariable("x{0}_{1}".format(i,j),lowBound=0,upBound=1,cat="Continuous") for j in range(n)] for i in range(n)]
    # objective function
    hillLP += np.sum(c*x)
    # antisymmetry constraint
    for i in range(n):
        for j in range(i+1,n):
                hillLP += x[i][j] + x[j][i] == 1
    # transitivity constraint
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if(j!=i and k!=j and k!=i):
                    hillLP += x[i][j] + x[j][k] + x[k][i] <= 2
    # solve problem
    hillLP.solve()
    pulp.LpStatus[hillLP.status]
    # optimal k value
    kstar = pulp.value(hillLP.objective)
    if(kstar==None):
        return 0.
    # worst k value
    x = np.zeros((n,n))
    for var in hillLP.variables():
        ind = var.name.find('_')
        x[int(var.name[1:ind]),int(var.name[ind+1:])] = var.varValue
    print(x)
    perm = np.sum(x,axis=1).argsort() # ascending order (worst ranking)
    permC = c[perm,:]
    permC = permC[:,perm]
    kworst = np.sum(permC*np.triu(np.ones((n,n))))
    # test
    perm = np.flip(perm)
    permC = c[perm,:]
    permC = permC[:,perm]
    print(np.sum(permC*np.triu(np.ones((n,n)))))
    # print kstar and kworst
    print(kstar)
    print(kworst)
    # call hillR_Pset
    #hillR_Pset(x,kstar)
    # return rankability
    if(kstar<TOL and kworst<TOL):
        return 0.
    else:
        return (kworst-kstar)/(kworst+kstar)
###############################################
###             hillR_Pset                  ###
###############################################
#   Computes Hillside Rankability P set.
###############################################
def hillR_Pset(x,kstar):
    """Computes Hillside Rankability P set."""
    perm = np.sum(x,axis=1).argsort()[::-1]
    permX = x[perm,:]
    permX = permX[:,perm]
    print(permX)
        
###############################################
###             hillR_Deprecated            ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
#def hillR_Deprecated(a):
#    """Computes Hillside Rankability Measure using scipy linprog."""
#    # build c matrix from data matrix a 
#    n = len(a)
#    c = np.zeros((n,n))
#    for i in range(n):
#        for j in range(n):
#            c[i,j] = np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int))
#    # reshape c matrix
#    c = c.reshape(n**2)
#    # create Aeq matrix and beq vector for Yoshi's constraint 1
#    con = 0
#    row = []; col = []; data = []
#    for j in range(n-1):
#        for i in range(j+1,n):
#            row.extend([con,con]); data.extend([1,1])
#            col.append(n*j+i); col.append(n*i+j)
#            con = con + 1
#    Aeq = csc_matrix((data, (row,col)), shape=(n*(n-1)//2,n*n))
#    beq = np.ones(n*(n-1)//2)
#    # create A matrix and b vector for Yoshi's constraint 2
#    con = 0
#    row = []; col = []; data = []
#    for i in range(n):
#        for l in range(n-1):
#            j = list(set(range(n)).difference({i}))
#            for m in range(n-2):
#                k = list(set(range(n)).difference({i,j[m]}))
#                col.append(n*j[l]+i); col.append(n*k[m]+j[l]); col.append(n*i+k[m])
#                row.extend([con,con,con]); data.extend([1,1,1])
#                con = con + 1
#    A = csc_matrix((data, (row,col)), shape=(n*(n-1)*(n-2),n*n))
#    b = 2*np.ones(n*(n-1)*(n-2))
#    # define lb and ub vectors (must be integer type)
#    lb = np.zeros(n*n,dtype=int)
#    ub = np.ones(n*n,dtype=int)
#    # force specific indices to be zero
#    index = list(range(0,n*n,n+1))
#    ub[index] = 0
#    # store bounds
#    bounds = []
#    for k in range(n*n):
#        bounds.append((lb[k],ub[k]))
#    # solve LP relaxation
#    res = linprog(c,A,b,Aeq,beq,bounds=bounds,method='interior-point',options={'sparse':True});
#    # optimal ordering (perm) and reversal (revPerm)
#    x = np.reshape(res.x,(n,n))
#    s = np.sum(x,axis=1)
#    revPerm = s.argsort()
#    perm = revPerm[::-1]
#    # optimal value (kstar) and reversal (kworst)
#    kstar = res.fun
#    c = c.reshape((n,n))
#    revPermC = c[revPerm,:]
#    revPermC = revPermC[:,revPerm]
#    kworst = np.sum(revPermC*np.triu(np.ones((n,n))))
#    # return rankability
#    if(kstar<TOL and kwosrt<TOL):
#        return 0.
#    else:
#        return (kworst-kstar)/(kworst+kstar)