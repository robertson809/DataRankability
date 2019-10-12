# NR: Numerical Range Plot
#
# Author: Thomas R. Cameron
# Date: 5/30/2019
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import itertools
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
        
        plt.subplot(122)
        plt.plot(np.real(f),np.imag(f))
        plt.plot(np.real(e),np.imag(e),'r*')
        #plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        
###############################################
###             Q Numerical Range           ###
###############################################
def qnr(l):
    """Plots q numerical range of graph Laplacian."""
    m, n = l.shape
    if(m!=n):
        print('Warning: matrix is non-square')
        return
    q = np.zeros((n,n-1))
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
    m = np.dot(np.transpose(q),np.dot(l,q))
    #print("******** Q Matrix ********")
    #print(m)
    nr(m)

###############################################
###             Unique Permutation          ###
###############################################
def unique_perm(a,n):
    ind = range(n)
    perm = []
    for i in itertools.permutations(ind):
        b = a[i,:]
        b = b[:,i]
        add = not any(np.array_equal(b,x) for x in perm)
        if(add):
            perm.append(b)
    return perm

###############################################
###             allQNR                      ###
###############################################
def allQNR(n):
    adj = []
    #find all isomorphically unique graphs
    for i in itertools.product([0, 1], repeat = n*n):
        a = np.reshape(np.array(i),(n,n))
        if(np.trace(a)==0):
            perm = unique_perm(a,n)
            add = not any(np.array_equal(p,x) for p in perm for x in adj)
            if(add):
                adj.append(a)
    print(len(adj)) 
            
    for a in adj:
        x = np.array([np.sum(a[i,:]) for i in range(n)])
        l = np.diag(x) - a
        #print("******** Graph Laplacian ********")
        #print(l)
        g = nx.DiGraph(a)
        nx.draw(g,with_labels=True, ax = plt.subplot(121))
        qnr(l)
        plt.show()

###############################################
###             impStar                     ###
###############################################
def impStar(n):
    a = np.zeros((n,n))
    for i in range(n-1):
        a[i,n-1] = -1
    g = nx.DiGraph(a)
    nx.draw(g)
    plt.show()
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    l = np.diag(x) - a
    qnr(l)
    
allQNR(3)
#impStar(4)