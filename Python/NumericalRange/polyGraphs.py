# Polygonal Graphs
#
# This module determines graphs with polygonal numerical range
#
# Author: Thomas R. Cameron
# Date: 11/24/2019
import itertools
import numpy as np
from math import pi as pi
from matplotlib import pyplot as plt

EPS = np.finfo(float).eps

###############################################
###             Convex Hull                 ###
###############################################
def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]
    
###############################################
###             checkHull                   ###
###############################################
def checkHull(convHull,x,y):
    tol = 10*EPS
    r0 = convHull[-1]
    res = False
    for k in range(len(convHull)):
        r1 = convHull[k]
        a0 = [r1[0]-r0[0],r1[1]-r0[1]]
        a1 = [x-r0[0],y-r0[1]]
        if(np.linalg.norm(a0)<=tol):
            res = res or (np.linalg.norm(a1)<=tol)
        else:
            a = np.zeros((2,2))
            a[:,0] = a0; a[:,1] = a1
            res = res or (np.linalg.matrix_rank(a,tol=tol)<2)
        r0 = r1
    return res
        
###############################################
###             Is Polygon                  ###
###############################################
def isPolygon(f,e):
    edges = []
    for eig in e:
        edges.append((eig.real,eig.imag))
    convHull = convex_hull(edges)
    res = True
    for z in f:
        res = res and checkHull(convHull,z.real,z.imag)
    return res

###############################################
###             Numerical Range             ###
###############################################
def nr(a):
    nv = 360
    n,_ = a.shape
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
    return f, np.linalg.eigvals(a)
    
###############################################
###             Plot Numerical Range        ###
###############################################
def pltNR(a):
    f,e = nr(a)
    plt.plot(np.real(f),np.imag(f))
    plt.plot(np.real(e),np.imag(e),'r*')
    plt.show()
    
###############################################
###             Q Numerical Range           ###
###############################################
def qnr(l):
    n,_ = l.shape
    q = np.zeros((n,n-1))
    for j in range(n-1):
        q[0:j+1,j] = 1
        q[j+1,j] = -(j+1)
        q[:,j] = q[:,j]/np.linalg.norm(q[:,j])
    a = np.dot(np.transpose(q),np.dot(l,q))
    return nr(a)
    
###############################################
###             Plot Q Numerical Range      ###
###############################################
def pltQNR(l):
    f,e = qnr(l)
    plt.plot(np.real(f),np.imag(f))
    plt.plot(np.real(e),np.imag(e),'r*')
    plt.show()
    
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
###             Poly Graphs                 ###
###############################################
def polyGraphs(n):
    adj = []
    count = 0
    for i in itertools.product([0, 1], repeat = n*n):
        a = np.reshape(np.array(i),(n,n))
        if(np.trace(a)==0):
            x = np.array([np.sum(a[i,:]) for i in range(n)])
            d = np.diag(x)
            l = d - a
            f,e = qnr(l)
            if(isPolygon(f,e)):
                perm = unique_perm(a,n)
                add = not any(np.array_equal(p,x) for p in perm for x in adj)
                if(add):
                    adj.append(a)
                    count = count + 1
                    print(count)
 
    for a in adj:
        x = np.array([np.sum(a[i,:]) for i in range(n)])
        l = np.diag(x) - a
        pltQNR(l)

###############################################
###             main                        ###
###############################################
#   test polygonal graph methods
###############################################
def main():
    polyGraphs(5)

if __name__ == '__main__':
    main()