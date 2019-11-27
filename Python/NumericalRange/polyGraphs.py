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
singleton_list = []
line_list = []
polygon_list = []
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
            s = np.linalg.svd(a,compute_uv=False)
            res = res or (s[1]<tol*s[0])
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
def pltQNR(l,graph_num):
    f,e = qnr(l)
    plt.plot(np.real(f),np.imag(f))
    plt.plot(np.real(e),np.imag(e),'r*')
    plt.title("Graph Number %d"%graph_num)
    plt.show()


def is_singleton(f):
    """
    checks to see if the shape described by the points in the array
    are really all the same point
    """
    return np.var(f) < 0.001


def is_line(f):
    """
    checks if the shape described by the points is a real line
    """
    return np.sum(np.absolute(np.imag(f))) < .001

    
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
<<<<<<< HEAD
def polyGraphs(n):
    mfile = open('matrices/adj'+str(n)+'.txt','w+')
=======
def polyGraphs(n, graph_list=[-1], disp = False):
>>>>>>> 5836dd137e24170230502daadd895af0cf4bbd6e
    adj = []
    count = 0
    graph_id = 0
    for i in itertools.product([0, 1], repeat = n*n):
        graph_id += 1
        a = np.reshape(np.array(i), (n, n))
        if np.trace(a) == 0 and ((graph_id in graph_list) or -1 in graph_list):
            x = np.array([np.sum(a[i, :]) for i in range(n)])
            d = np.diag(x)
            l = d - a
            f,e = qnr(l)
            if is_singleton(f):
                singleton_list.append(graph_id)
            elif is_line(f):
                line_list.append(graph_id)
            elif isPolygon(f, e):
                perm = unique_perm(a, n)
                add = not any(np.array_equal(p, x) for p in perm for x in adj)
                if add:
                    adj.append(a)
                    polygon_list.append(graph_id)
                    count = count + 1
<<<<<<< HEAD
                    print(count)
    for a in adj:
        for i in range(n):
            for j in range(n-1):
                mfile.write("%d "%a[i,j])
            mfile.write("%d\n"%a[i,n-1])
        mfile.write("\n")
    mfile.close()
    
###############################################
###             display Poly Graphs         ###
###############################################
def dispPolyGraphs(n):
    mfile = open('matrices/adj'+str(n)+'.txt')
    lineList = mfile.readlines()
    a = np.zeros((n,n))
    i = 0
    graph_num = 1
    for row in lineList:
        row = row.split(" ")
        if(len(row)<n):
            x = np.array([np.sum(a[i,:]) for i in range(n)])
            l = np.diag(x) - a
            pltQNR(l,graph_num)
            a = np.zeros((n,n))
            i = 0
            graph_num = graph_num + 1
        else:
            a[i,:] = [eval(row[j]) for j in range(n)]
            i = i + 1
=======
                    print('polygon {} is graph_id {}'.format(count, graph_id))
                    if disp:
                        lt.subplot(122)
                        plt.plot(np.real(f), np.imag(f))
                        plt.plot(np.real(e), np.imag(e), 'r*')
                        #  plt.gca().set_aspect('equal', adjustable='box')
                        plt.show()
 
    for a in adj:
        x = np.array([np.sum(a[i,:]) for i in range(n)])
        l = np.diag(x) - a
        pltQNR(l)
    print('the singletons are at', singleton_list)
    print('the lines are at', line_list)
    print('the polygons are at', polygon_list)
>>>>>>> 5836dd137e24170230502daadd895af0cf4bbd6e

###############################################
###             main                        ###
###############################################
#   test polygonal graph methods
###############################################
def main():
<<<<<<< HEAD
    #polyGraphs(5)
    dispPolyGraphs(5)
=======
    polyGraphs(4)
    #polyGraphs(4, [323, 2507, 4741, 6357, 14687, 14791])
>>>>>>> 5836dd137e24170230502daadd895af0cf4bbd6e

if __name__ == '__main__':
    main()

#singleton_list = [1, 2185, 4369, 6553, 8707, 10891, 13075, 15259, 16453, 18637, 20821, 23005, 25159, 27343, 29527, 31711]
#line_list = [15, 19, 205, 209, 223, 261, 279, 469, 577, 591, 595, 837, 855, 2203, 2445, 2449, 2463, 2571, 2761,
# 2779, 2817, 2831, 2835, 3021, 3025, 3039, 4105, 4123, 4313, 4365, 4383, 4573, 4681, 4699, 4941, 4945, 4959,
# 6921, 6939, 7129, 8321, 8335, 8339, 8581, 8599, 8897, 8911, 8915, 8967, 9157, 9175, 11137, 11151, 11155,
# 12425, 12443, 12685, 12689, 12703, 12811, 13001, 13019, 13057, 13071, 13261, 13265, 13279, 15241, 16471,
# 18433, 18447, 18451, 18641, 18655, 18693, 18711, 18901, 19009, 19023, 19027, 19269, 19287, 20557, 20561,
# 20575, 22537, 22555, 22745, 22797, 22801, 22815, 23113, 23131, 23373, 23377, 23391, 24583, 24773, 24791,
# 26753, 26767, 26771, 27013, 27031, 27139, 27329, 27347, 27399, 27589, 27607, 28673, 28687, 28691, 28877,
# 28881, 28895, 28933, 28951, 29141, 29249, 29263, 29267, 29509, 30857, 30875, 31117, 31121, 31135, 31243,
# 31433, 31451, 31489, 31503, 31507, 31693, 31697]
#poly_list = [323, 2507, 4741, 6357, 14687, 14791]