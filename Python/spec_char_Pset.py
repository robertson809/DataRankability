# Spectral Characterization P Set
# Thomas R. Cameron
# 3/12/2019
import copy
import itertools
import numpy as np

# machine epsilon
eps = np.finfo(float).eps

###############################################
###             eigM2                       ###
###############################################
#   Matching distance between spectrum e and s.
#   Returns min and indices where min occured.
###############################################
def eigM2(e,s):
    """Matching distance between spectrum e and s."""
    perm = list(itertools.permutations(s))
    arr = [max(abs(perm[k]-e)) for k in range(len(perm))]
    m = min(arr)
    ind = [k for k in range(len(arr)) if m==arr[k]]
    return m, ind
    
###############################################
###             vecM2                       ###
###############################################
#   Matching distance between eigenvectors in
#   v and s. Returns min and indices where min
#   occured.
###############################################
def vecM2(v,s):
    """Matching distance between eigenvectors in v and s"""
    perm = list(itertools.permutations(range(len(s))))
    arr = [max([subD(s[perm[i],:][:,j],v[:,j]) for j in range(len(v))]) for i in range(len(perm))]
    m = min(arr)
    ind = [k for k in range(len(arr)) if abs(m-arr[k])<=eps*m]
    for k in range(len(ind)):
        print(perm[ind[k]])
    return m, ind
    
###############################################
###             Main                        ###
###############################################
#   Used for testing functions defined above.
###############################################
def main():
    # graph Laplacians
    lap = [np.array([[5,-1,-1,-1,-1,-1],[0,3,-1,0,-1,-1],[0,0,2,0,-1,-1],[0,-1,-1,4,-1,-1],[0,0,0,0,1,-1],[0,0,0,0,0,0]]),
            np.array([[5,-1,-1,-1,-1,-1],[0,3,0,-1,-1,-1],[-1,0,4,-1,-1,-1],[0,0,0,2,-1,-1],[0,0,0,0,1,-1],[0,0,0,0,0,0]]),
            np.array([[3,-1,0,0,-1,-1],[0,2,-1,-1,0,0],[0,-1,1,0,0,0],[-1,0,0,2,0,-1],[0,0,0,-1,1,0],[-1,-1,-1,0,-1,4]]),
            np.array([[3,-1,-1,-1,0,0],[0,1,-1,0,0,0],[0,0,0,0,0,0],[0,0,0,2,-1,-1],[0,0,0,0,1,-1],[0,0,0,0,0,0]]),
            np.array([[2,-1,0,0,0,-1],[0,2,-1,-1,0,0],[0,-1,1,0,0,0],[-1,0,0,2,0,-1],[0,0,0,0,0,0],[0,-1,-1,0,0,2]]),
            np.array([[1,-1,0,0,0,0],[0,1,-1,0,0,0],[0,0,1,-1,0,0],[0,0,0,1,-1,0],[0,0,0,0,1,-1],[-1,0,0,0,0,1]]),
            np.array([[5,-1,-1,-1,-1,-1],[-1,5,-1,-1,-1,-1],[-1,-1,5,-1,-1,-1],[-1,-1,-1,5,-1,-1],[-1,-1,-1,-1,5,-1],[-1,-1,-1,-1,-1,5]]),
            np.zeros((6,6))
            ]
    # name of graphs
    nam = ['Dominance Graph','Dominance+Perturbation','Perturbed Random Graph','Nearly Disconnected','Random','Cyclic','Completely Connected','Empty Graph']
    # test vecM2
    n = 6
    s1 = np.array([n-k for k in range(1,n+1)])
    s2 = np.identity(n)+0j*np.identity(n)
    for k in range(1,n):
        s2[:,k] = s2[:,k] + s2[:,k-1]
    print(nam[4])
    l = lap[4]
    e, v = np.linalg.eig(l)
    print('vecM2 results:')
    m, ind = vecM2(v,s2)
    print(m)
    print(ind)

main()