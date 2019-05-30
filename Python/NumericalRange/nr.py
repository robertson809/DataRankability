# NR: Numerical Range Plot
#
# Author: Thomas R. Cameron
# Date: 5/30/2019
import numpy as np
from matplotlib import pyplot as plt
from math import pi as pi

###############################################
###             Numerical Range             ###
###############################################
def nr(a):
    """Plots numerical range of a matrix with its eigenvalues."""
    nv = 120
    m, n = a.shape
    if(m!=n):
        print('Warning: matrix is non-square')
        return
    else:
        e = np.linalg.eigvals(a)
        f = []
        for k in range(1,nv+1):
            z = np.exp(2*pi*1j*(k-1)/nv)
            a1 = z*a
            a2 = (a1 + np.transpose(np.conjugate(a1)))/2
            w, v = np.linalg.eig(a2)
            ind = np.argsort(w)
            w = w[ind]
            v = v[:,ind]
            v = v[:,n-1]
            f.append(np.dot(np.conjugate(v),np.dot(a,v))/np.dot(np.conjugate(v),v))
        f.append(f[0])
        f = np.array(f)
        plt.plot(np.real(f),np.imag(f))
        plt.plot(np.real(e),np.imag(e),'r*')
        plt.show()
        
###############################################
###             Simod Graphs                ###
###############################################
def simod_graphs():
    # graph names
    nam = ['Dominance Graph','Dominance+Perturbation','Perturbed Random Graph','Nearly Disconnected','Random','Cyclic','Completely Connected','Empty Graph']
    # adjacency matrices
    adj = [np.array([[0.,1,1,1,1,1],[0,0.,1,0,1,1],[0,0,0.,0,1,1],[0,1,1,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
            np.array([[0.,1,1,1,1,1],[0,0.,0,1,1,1],[1,0,0.,1,1,1],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0]]),
            np.array([[0.,1,0,0,1,1],[0,0.,1,1,0,0],[0,1,0.,0,0,0],[1,0,0,0.,0,1],[0,0,0,1,0.,0],[1,1,1,0,1,0.]]),
            np.array([[0.,1,1,1,0,0],[0,0.,1,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
            np.array([[0.,1,0,0,0,1],[0,0.,1,1,0,0],[0,1,0.,0,0,0],[1,0,0,0.,0,1],[0,0,0,0,0.,0],[0,1,1,0,0,0.]]),
            np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,0],[0,0,0.,1,0,0],[0,0,0,0.,1,0],[0,0,0,0,0.,1],[1,0,0,0,0,0.]]),
            np.array([[0.,1,1,1,1,1],[1,0.,1,1,1,1],[1,1,0.,1,1,1],[1,1,1,0.,1,1],[1,1,1,1,0.,1],[1,1,1,1,1,0.]]),
            np.zeros((6,6))
            ]
    # laplacian matrices
    lap = []
    for k in range(len(adj)):
        a = adj[k]
        n = len(a)
        x = np.array([np.sum(a[i,:]) for i in range(n)])
        d = np.diag(x)
        l = d - a;
        lap.append(l)
    # numerical range test
    for k in range(len(lap)):
        # write name
        print(nam[k])
        # graph laplacian
        l = lap[k]
        n = len(l)
        # orthonormal matrix q
        q = np.zeros((n,n-1))
        for j in range(n-1):
            q[0:j+1,j] = 1
            q[j+1,j] = -(j+1)
            q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
        # projection transformation
        l = 0.5*np.dot(np.transpose(q), np.dot(l,q))
        # numerical range of l
        nr(l)

###############################################
###             Dominance Graphs            ###
###############################################
def dominance_graphs():
    for n in range(2,11):
        # perfect dominance graph on n vertices
        l=np.zeros((n,n))
        for i in range(n):
            l[i,i] = n-(i+1)
            for j in range(i+1,n):
                l[i,j] = -1
        # orthonormal matrix q
        q = np.zeros((n,n-1))
        for j in range(n-1):
            q[0:j+1,j] = 1
            q[j+1,j] = -(j+1)
            q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
        # projection transformation
        l = 0.5*np.dot(np.transpose(q), np.dot(l,q))
        # numerical range of l
        nr(l)
        

#simod_graphs()
dominance_graphs()