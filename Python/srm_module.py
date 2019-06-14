# SRM: Spectral Rankability Measure
#
# This module contains the functions necessary for measuring the rankability of a dataset.
# In particular, the dataset should be captured as a directed graph with binary weights.
# Given the corresponding adjacency matrix, a rankability measure is returned based on the 
# spectral characterization of the Laplacian.
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
import itertools
import numpy as np

def inv(perm):
    inverse = [0] * len(perm)
    for i, p in enumerate(perm):
        inverse[p] = i
    return inverse

###############################################
###             Ranking                     ###
###############################################
#   Uses eigenvalue and eigenvector information 
#   to produce ranking of data. 
###############################################
def ranking(a):
    """Uses eigenvalue and eigenvector information to produce ranking of data."""
    # size, adjacency, degree, and laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # eigenvalue and eigenvector information
    vec_s = np.zeros((n,n))
    for j in range(n):
        vec_s[0:j+1,j] = 1
        vec_s[:,j] = vec_s[:,j]/np.linalg.norm(vec_s[:,j])
    e, v = np.linalg.eig(l)
    # sort degree (descending)
    ind1 = (-x).argsort()[:n]
    x = x[ind1]
    print(inv(ind1))
    # sort eigenvalues and eigenvectors against degree
    perm = list(itertools.permutations(range(n)))
    perm = [list(perm[k]) for k in range(len(perm))]
    match = [np.linalg.norm(e[perm[k]]-x) for k in range(len(perm))]
    m = min(match)
    ind2 = perm[match.index(m)]
    e = e[ind2]
    v = v[:,ind2]
    # sort eigenvectors against vec_s
    match = [np.linalg.norm(v[perm[k],:]-vec_s,ord=1) for k in range(len(perm))]
    m = min(match)
    ind3 = perm[match.index(m)]
    v = v[ind3,:]
    # ranking
    ind3 = inv(ind3)
    ind = [ind3[ind1[k]] for k in range(n)]
    return inv(ind)
    
###############################################
###             Matching                    ###
###############################################
#   Matching distance between sets e and s.
###############################################
def Matching(e,s):
    """Matching distance between sets e and s."""
    perm = list(itertools.permutations(e))
    return min([max(abs(perm[k]-s)) for k in range(len(perm))])
    
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
###             acyclicR                    ###
###############################################
#   Computes Acyclic Rankability Measure.
###############################################
def acyclicR(a):
    """Computes Acyclic Rankability Measure."""
    # given graph Laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # eigenvalues of given graph Laplacian
    e = np.linalg.eigvals(l)
    # rankability measure
    return Hausdorff(e,x)/max(x)
    
###############################################
###             matchR                      ###
###############################################
#   Computes Matching Rankability Measure.
###############################################
def matchR(a):
    """Computes Matching Rankability Measure."""
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
    return 1. - ((Matching(e,s)+Matching(x,s))/(2*(n-1)))
    
###############################################
###             spec2R                      ###
###############################################
#   Computes Spectral Rankability Measure for
#   double round robins.
###############################################
def spec2R(a):
    """Computes Spectral Rankability Measure for double round robins."""
    # given graph Laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # perfect dominance graph spectrum and out-degree
    s = np.array([2*(n-k) for k in range(1,n+1)])
    # eigenvalues of given graph Laplacian
    e = np.linalg.eigvals(l)
    # rankability measure
    return 1. - ((Hausdorff(e,s)+Hausdorff(x,s))/(4*(n-1)))
    
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
###             algCon                      ###
###############################################
#   Compute the algebraic connectivity.
###############################################
def algCon(a):
    """Compute the algebraic connectivity."""
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    q = np.zeros((n,n-1))
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
    e = np.linalg.eigvalsh(0.5*np.dot(np.transpose(q), np.dot(l+np.transpose(l),q)))
    return np.amin(e)
    
###############################################
###             betaCon                     ###
###############################################
#   Compute the related quantity beta.
###############################################
def betaCon(a):
    """Compute the related quantity beta."""
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    q = np.zeros((n,n-1))
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
    e = np.linalg.eigvalsh(0.5*np.dot(np.transpose(q), np.dot(l+np.transpose(l),q)))
    return np.amax(e)
    
###############################################
###             rankA                       ###
###############################################
#   Compute rankability measure with respect
#   to algebraic connectivity. 
###############################################
def rankA(a):
    """Compute rankability measure with respect to algebraic connectivity."""
    n = len(a)
    s = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            s[i,j] = 1
    return abs(algCon(a)-algCon(s))
    
###############################################
###             rankB                       ###
###############################################
#   Compute rankability measure with respect
#   to related quantity beta. 
###############################################
def rankB(a):
    """Compute rankability measure with respect to related quantity beta."""
    n = len(a)
    s = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            s[i,j] = 1
    return abs(betaCon(a)-betaCon(s))
    
###############################################
###             connR                       ###
###############################################
#   Computes Connectivity Rankability Measure.
###############################################
def connR(a):
    """Computes Connectivity Rankability Measure."""
    # given graph Laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # perfect dominance graph Laplacian
    s = np.zeros((n,n))
    for i in range(n):
        s[i,i] = n-(i+1)
        for j in range(i+1,n):
            s[i,j] = -1
    # orthonormal matrix q
    q = np.zeros((n,n-1))
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
    # connectivity of given graph
    e = np.linalg.eigvalsh(0.5*np.dot(np.transpose(q), np.dot(l+np.transpose(l),q)))
    emin = np.amin(e)
    emax = np.amax(e)
    # connectivity of perfect dominance graph
    e = np.linalg.eigvalsh(0.5*np.dot(np.transpose(q), np.dot(s+np.transpose(s),q)))
    smin = np.amin(e)
    smax = np.amax(e)
    # rankability measure
    return (abs(smin-emin) + abs(smax-emax))/n