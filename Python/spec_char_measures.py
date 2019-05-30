# Spectral Characterization Measures
# Thomas R. Cameron
# 3/16/2019
import copy
import itertools
import numpy as np

#####################################################################################################################
#                 1D Subspace Distance                                                                              #
#####################################################################################################################

###############################################
###             qrV                         ###
###############################################
#   QR decomposition of a single vector. Return
#   unitary matrix q such that the first column 
#   of q is parallel to v and the other columns
#   are orthogonal to v.
#   Note the values of v change. 
###############################################
def qrV(v):
    """QR decomposition of a single vector"""
    n = len(v)
    q = np.identity(n) + 1j*np.zeros((n,n))
    tempV = copy.deepcopy(v)
    for i in range(1,n):
        r = np.linalg.norm([tempV[0],tempV[i]])
        if r>0:
            c = tempV[0]/r
            s = tempV[i]/r
            u = np.array([np.conj([c, s]), [-s, c]])
            q[[0,i],:] = np.matmul(u,q[[0,i],:])
            tempV[[0,i]] = [r,0]
    return np.transpose(np.conj(q))

###############################################
###             subD                        ###
###############################################
#   Distance between 1-D subspaces spanned by
#   u and v. 
###############################################
def subD(u,v):
    """Distance between 1-D subspace spanned by u and v"""
    n = len(u)
    # q = np.random.rand(n,n) + 1j*np.random.rand(n,n)
    # q[:,0] = copy.deepcopy(v)
    # q, _ = np.linalg.qr(q)
    q = qrV(v)
    rho = np.linalg.norm(u)
    if rho>0:
        u = np.conj(u/rho)
    return np.linalg.norm(np.dot(u,q[:,1:n]))

#####################################################################################################################
#                 Matching Distance Rankability Measures                                                            #
#####################################################################################################################

###############################################
###             eigM                        ###
###############################################
#   Matching distance between spectrum e and s.
###############################################
def eigM(e,s):
    """Matching distance between spectrum e and s."""
    perm = list(itertools.permutations(e))
    return min([max(abs(perm[k]-s)) for k in range(len(perm))])
    
###############################################
###             vecM                        ###
###############################################
#   Matching distance between eigenvectors in
#   v and s. 
###############################################
def vecM(v,s):
    """Matching distance between eigenvectors in v and s"""
    perm = list(itertools.permutations(range(len(v))))
    return min([max([subD(v[perm[i],:][:,j],s[:,j]) for j in range(len(v))]) for i in range(len(perm))])
    
###############################################
###             rankM                       ###
###############################################
#   Compute rankability measure with respect
#   to matching distance.
###############################################
def rankM(l):
    """Compute rankability measure with respect to matching distance."""
    n = len(l)
    s1 = np.array([n-k for k in range(1,n+1)])
    s2 = np.identity(n)
    for k in range(1,n):
        s2[:,k] = s2[:,k] + s2[:,k-1]
    e, v = np.linalg.eig(l)
    return eigM(e,s1) + vecM(v,s2)
    
#####################################################################################################################
#                 Hausdorff Distance Rankability Measures                                                           #
#####################################################################################################################
    
###############################################
###             eigH                       ###
###############################################
#   Hausdorff distance between eigenvalues in e
#   and in s. 
###############################################
def eigH(e,s):
    """Hausdorff distance between eigenvalues in e and in s"""
    def _eigSV(e,s):
        return max([min([abs(e[i]-s[j]) for j in range(len(s))]) for i in range(len(e))])
    return max(_eigSV(e,s),_eigSV(s,e))
    
###############################################
###             vecH                       ###
###############################################
#   Hausdorff distance between eigenvectors in v
#   and in s. 
###############################################
def vecH(v,s):
    """Hausdorff distance between eigenvectors in v and in s"""
    def _vecSV(v,s):
        return max([min([subD(v[:,i],s[:,j]) for j in range(len(s))]) for i in range(len(v))])
    return max(_vecSV(v,s),_vecSV(s,v))
    
###############################################
###             rankH                       ###
###############################################
#   Compute rankability measure with respect
#   to Hausdorff distance.
###############################################
def rankH(l):
    """Compute rankability measure with respect to Hausdorff distance."""
    n = len(l)
    s1 = np.array([n-k for k in range(1,n+1)])
    s2 = np.identity(n)
    for k in range(1,n):
        s2[:,k] = s2[:,k] + s2[:,k-1]
    e, v = np.linalg.eig(l)
    return eigH(e,s1) + vecH(v,s2)

    
###############################################
###             Main                        ###
###############################################
#   Used for testing functions defined above.
###############################################
def main():
    # graph Laplacians
    lap = [np.array([[5.,-1.,-1.,-1.,-1.,-1.],[0.,3.,-1.,0.,-1.,-1.],[0.,0.,2.,0.,-1.,-1.],[0.,-1.,-1.,4.,-1.,-1.],[0.,0.,0.,0.,1.,-1.],[0.,0.,0.,0.,0.,0.]]),
            np.array([[5.,-1.,-1.,-1.,-1.,-1.],[0.,3.,0.,-1.,-1.,-1.],[-1.,0.,4.,-1.,-1.,-1.],[0.,0.,0.,2.,-1.,-1.],[0.,0.,0.,0.,1.,-1.],[0.,0.,0.,0.,0.,0.]]),
            np.array([[3.,-1.,0.,0.,-1.,-1.],[0.,2.,-1.,-1.,0.,0.],[0.,-1.,1.,0.,0.,0.],[-1.,0.,0.,2.,0.,-1.],[0.,0.,0.,-1.,1.,0.],[-1.,-1.,-1.,0.,-1.,4.]]),
            np.array([[3.,-1.,-1.,-1.,0.,0.],[0.,1.,-1.,0.,0.,0.],[0.,0.,0.,0.,0.,0.],[0.,0.,0.,2.,-1.,-1.],[0.,0.,0.,0.,1.,-1.],[0.,0.,0.,0.,0.,0.]]),
            np.array([[2.,-1.,0.,0.,0.,-1.],[0.,2.,-1.,-1.,0.,0.],[0.,-1.,1.,0.,0.,0.],[-1.,0.,0.,2.,0.,-1.],[0.,0.,0.,0.,0.,0.],[0.,-1.,-1.,0.,0.,2.]]),
            np.array([[1.,-1.,0.,0.,0.,0.],[0.,1.,-1.,0.,0.,0.],[0.,0.,1.,-1.,0.,0.],[0.,0.,0.,1.,-1.,0.],[0.,0.,0.,0.,1.,-1.],[-1.,0.,0.,0.,0.,1.]]),
            np.array([[5.,-1.,-1.,-1.,-1.,-1.],[-1.,5.,-1.,-1.,-1.,-1.],[-1.,-1.,5.,-1.,-1.,-1.],[-1.,-1.,-1.,5.,-1.,-1.],[-1.,-1.,-1.,-1.,5.,-1.],[-1.,-1.,-1.,-1.,-1.,5.]]),
            np.zeros((6,6))
            ]
    # name of graphs
    nam = ['Dominance Graph','Dominance+Perturbation','Perturbed Random Graph','Nearly Disconnected','Random','Cyclic','Completely Connected','Empty Graph']
    # compute rankability of graphs
    s = np.array([5.,4.,3.,2.,1.,0.])
    for k in range(len(nam)):
        print(nam[k]+':')
        e, v = np.linalg.eig(lap[k])
        print(eigH(e,s),eigM(e,s))
    #    print('matching distance rankability = '+str(rankM(lap[k])))
    #    print('Hausdorff distance rankability = '+str(rankH(lap[k])))

main()