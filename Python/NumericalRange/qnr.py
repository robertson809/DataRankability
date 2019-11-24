# NR: Numerical Range Plot
#
# Author: Thomas R. Cameron, Michael Robertson
# Date: 5/30/2019
import numpy as np
from scipy.spatial import ConvexHull
from matplotlib import pyplot as plt
import networkx as nx
import itertools
from math import pi as pi
from operator import itemgetter
# Global variables are realllly bad practice but otherwise
# I'd have to pass things all over the place
from scipy.spatial.qhull import ConvexHull
from numpy.linalg import matrix_rank as matrix_rank
from numpy.linalg import det as det

singleton_index_list = []
line_index_list = []
poly_index_list = []


def nr(a, graph_num, disp):
    """
    Plots numerical range of a matrix with its eigenvalues.
    :param a: the adjacency matrix of the graph
    :param graph_num: graph id in our unique permutation ordering
    :param disp: Boolean -- the choice to plot the graph and nr or not
    """
    nv = 120  # precision / sampling rate
    m, n = a.shape
    assert (m == n)
    e = np.linalg.eigvals(a)
    f = []
    for k in range(1, nv + 1):
        z = np.exp(2 * pi * 1j * (k - 1) / nv)  # nv roots of unity
        a1 = z * a
        # A_2 is Hermitian part, and the NR of A_2 is the Real part of NR(A)
        a2 = (a1 + np.transpose(np.conjugate(a1))) / 2
        eigvals, eigvecs = np.linalg.eig(a2)
        ind = np.argsort(eigvals)
        eigvals = eigvals[ind]  # sorts the array
        eigvecs = eigvecs[:, ind]
        eigvecs = eigvecs[:, n - 1]
        #  gives a point on the nr, x = v^*Av / ||v||
        f.append(np.dot(np.conjugate(eigvecs), np.dot(a, eigvecs))
                 / np.dot(np.conjugate(eigvecs), eigvecs))
    f.append(f[0])
    f = np.array(f)
    if is_singleton(f):
        singleton_index_list.append(graph_num)
    elif is_line(f):
        line_index_list.append(graph_num)
    elif is_polygon(f, a):
        poly_index_list.append(graph_num)
    if disp:
        plt.subplot(122)
        plt.plot(np.real(f), np.imag(f))
        plt.plot(np.real(e), np.imag(e), 'r*')
        #  plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


def qnr(l, graph_num, disp):
    """
    Plots q numerical range of graph Laplacian
    :param l: Laplacian graph
    :param graph_num: graph id in our unique permutation ordering
    :param disp: Boolean -- the choice to plot the graph and nr or not
    """
    m, n = l.shape
    assert (m == n)
    q = np.zeros((n, n - 1))
    for j in range(n - 1):
        q[0:j + 1, j] = 1
        q[j + 1, j] = -(j + 1)
        q[:, j] = q[:, j] / np.linalg.norm(q[:, j])
    m = np.dot(np.transpose(q), np.dot(l, q))
    nr(m, graph_num, disp)


def unique_perm(a, n):
    """
    checks if a is a unique permutation, or if it is a duplicate of a
    graph in the set n
    :param a:
    :param n:
    :return:
    """
    ind = range(n)
    perm = []
    for i in itertools.permutations(ind):
        b = a[i, :]
        b = b[:, i]
        add = not any(np.array_equal(b, x) for x in perm)
        if add:
            perm.append(b)
    return perm


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


def linearly_dep(evs):
    ones = np.ones((1, (int(evs.size / 2))))
    area_mat = np.append(evs, ones, axis=0)
    area = det(area_mat)
    return area <= .001


def euler_sort(evs):
    return np.argsort(np.angle(evs))


def in_between(a, b, x):
    return a < x < b or b < x < a or abs(x - a) < .0001 or abs(x - b) < .0001


def is_polygon(f, l):
    """
    If the NR is a n-gon, then it will have n corners, which must be the n eigenvalues.
    Therefore, we must simply test if NR(A) = convex hull (sigma(A)) to see if the NR
    is a polygon -- this won't miss anything.

    Test with example cycles who have polygon NRs
    ##get the points from convexhull next
    :param f: the points on the boundary of the numerical range,
    :param l: the graph laplacian
    :return bool : whether the graph is a polygon
    """
    # find convex hull of eig l
    evs = np.linalg.eigvals(l)
    twod_evs = np.column_stack((evs.real, evs.imag))
    ordered_vertices = twod_evs[euler_sort(evs)]
    on_line = False
    count = 0
    # print(f)
    for num in f:
        count += 1
        on_line = False
        for i in range(len(ordered_vertices)):
            if i == len(ordered_vertices) - 1:
                m = 0
            else:
                m = i + 1
            if in_between(ordered_vertices[i][0], ordered_vertices[m][0], num.real) and \
                    in_between(ordered_vertices[i][1], ordered_vertices[m][1], num.imag):
                a = np.asarray([[num.real - ordered_vertices[i][0], ordered_vertices[m][0] -
                                 ordered_vertices[i][0]],
                                [num.imag - ordered_vertices[i][1],
                                 ordered_vertices[m][1] - ordered_vertices[i][1]]])
                if matrix_rank(a, tol=1e-14) == 1:
                    print('point {} on line {}'.format(count, i))
                    on_line = True
                    break
                else:
                    print('not on line ', i)
        if not on_line:
            return False
    print('is a polygon')
    return True


def allQNR(n, r_graph_num=-1, disp=False):
    """
    Finds and prints ALL the restricted numerical ranges of graphs on n vertices. Does not consider uniqueness
    around isomorphism
    :param n: the number of vertices
    :param r_graph_num: potential to specify a graph or list of graphs rather than all graphs, default -1
                        prints all graphs
    :param disp: the option to display pictures of the graphs generated
    :return:
    """
    adj = []
    # produces a list of flattened matrices with 1,0 entries
    for i in itertools.product([0, 1], repeat=n * n):
        a = np.reshape(np.array(i), (n, n))  # don't give a shit if this is unique or not
        if np.trace(a) == 0:
            adj.append(a)

    if r_graph_num != -1:  # turn adj into a singleton or shortened list
        if type(r_graph_num) == int:
            g = adj[r_graph_num]
            adj = [g]
        if type(r_graph_num) == list:
            adj = [adj[num] for num in r_graph_num]

    graph_num = 0
    for a in adj:
        x = np.array([np.sum(a[i, :]) for i in range(n)])
        l = np.diag(x) - a
        if disp:
            if r_graph_num == -1:
                plt.title('Graph {}'.format(graph_num))
            elif type(r_graph_num) == int:
                plt.title('Graph {}'.format(r_graph_num))
            elif type(r_graph_num) == list:
                plt.title('Graph {}'.format(r_graph_num[graph_num]))
            g = nx.DiGraph(a)
            nx.draw(g, with_labels=True, ax=plt.subplot(121))
        graph_num += 1
        qnr(l, graph_num, disp)


def isoQNR(n, r_graph_num=-1, disp=True):
    """
    Finds and prints ALL the restricted numerical ranges of graphs on n vertices. Does not consider uniqueness
    around isomorphism
    print the requested graph-numerical range pair
    :param n: the number of vertices the graph should be on
    :param r_graph_num: potential to specify a graph or list of graphs rather than all graphs, default -1
                        prints all graphs
    :param disp: the option to display pictures of the graphs generated
    """
    adj = []  # adjacency matrix of all i-unique graphs
    # find all isomorphically unique adjacency
    for i in itertools.product([0, 1], repeat=n * n):
        a = np.reshape(np.array(i), (n, n))
        if (np.trace(a) == 0):
            perm = unique_perm(a, n)
            add = not any(np.array_equal(p, x) for p in perm for x in adj)
            if (add):
                adj.append(a)
    print('There are {} isomorphically unique graphs '
          'with {} vertices'.format(len(adj), n))

    if r_graph_num != -1:  # turn adj into a singleton to only return one graph
        if type(r_graph_num) == int:
            g = adj[r_graph_num]
            adj = [g]
        if type(r_graph_num) == list:
            adj = [adj[num] for num in r_graph_num]

    graph_num = 0
    for a in adj:
        x = np.array([np.sum(a[i, :]) for i in range(n)])
        l = np.diag(x) - a
        print("******** Graph Laplacian #{} ********".format(graph_num))
        print(l)
        g = nx.DiGraph(a)
        nx.draw(g, with_labels=True, ax=plt.subplot(121))
        if r_graph_num == -1:
            plt.title('Graph {}'.format(graph_num))
        elif type(r_graph_num) == int:
            plt.title('Graph {}'.format(r_graph_num))
        elif type(r_graph_num) == list:
            plt.title('Graph {}'.format(r_graph_num[graph_num]))
        qnr(l, graph_num, disp)
        # plt.show()
        # print('showing the numerical range of just L')
        # nr(l, graph_num)
        graph_num += 1

    # The imploding stars for 3 graphs are 0, 6, 13 and 15


# for 4 they are 0, 76, 176, 213, and 217
def impStar(n):
    """
    Creates imploding star Graph Laplacians
    :param n: Number of vertices in the graph
    """
    a = np.zeros((n, n))
    for i in range(n - 1):
        a[i, n - 1] = -1
    g = nx.DiGraph(a)
    nx.draw(g)
    plt.show()
    x = np.array([np.sum(a[i, :]) for i in range(n)])
    lap = np.diag(x) - a
    qnr(lap)


baseball = [15, 20, 39]
pseduocycles = [27, ]
lines = [21]
three_IS = [0, 6, 13, 15]
four_IS = [0, 76, 176, 213, 217]
# two exploding star for five vertices.
# look at k exploding stars and lines
# what are lines? We have a theory that they are either exploding stars
# or they are k -- imploding stars unioned with disjoint isolated vertices.

# check to see if the 2 exploding star on n vertices is always the line from 0 to n
# or it's the 3 exploding star, or it's the n -2 exploding

######RESULTS######
# it is the 2 exploding that has the line from [0,n]
# what about imploding stars unioned with isolated vertices?
# for n= 3, imploding(1)  + isolated is just one edge nr = elipse
# imploding(2) + isolated is 2 cycle, [0, 2]
# imploding(3) + doesn't exist
# for n = 4, imploding(1) + isolated is qnr([[1,-1,0,0],[0,1,-1,0],[0,0,0,0],[0,0,0,0]]), lopsided elipse, imploding(2) + isolated is qnr([[2,-1,-1,0],[0,1,-1,0],[0,-1,1,0],[0,0,0,0]]), ellipse, imploding(3) + isolated is


# to finish my proof to show that the eigenvalues are real, take the matrix in frobenius
# normal form, and then look at it's imploding k complete graph sections and then its
# pointing to everything else section. One you know the form of, the other is just a upper triangularmatrix so
# you know the eignvalues are k because the diangonal lines are k

# isoQNR(4, r_graph_num= 76)
# isoQNR(4, r_graph_num = four_IS)
# isoQNR(3, r_graph_num = [0, 2, 3, 6, 8, 10, 13, 15])
# isoQNR(3)
# qnr(np.asarray([[5,-1,-1,-1,-1,-1],[-1,5,-1,-1,-1,-1],[-1,-1,5,-1,-1,-1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]), -1, True)
# isoQNR(4, 125)
# qnr(np.asarray([[1,-1,0],[-1,2,-1],[0,-1,1]]), -1, True)
# qnr(np.asarray([[1,-1,0,0,0],[-1,2,-1,0,0],[0,-1,2,-1,0],[0,0,-1,2,-1],[0,0,0,-1,1]]),-1,True)
# cycle polygon


# qnr(np.asarray([[1, 0, 0, 0, -1], [-1, 1, 0, 0, 0], [0, -1, 1, 0, 0], [0, 0, -1, 1, 0], [0, 0, 0, -1, 1]]), -1, True)
# qnr(np.asarray([[1, 0, 0, -1], [0, 2, -1, -1], [-1, 0, 2, -1], [-1, 0, 0, 1]]), -1, True)

# isoQNR(4)
allQNR(4, disp=True)
# isoQNR(4, [0, 3, 4, 19, 21, 23, 56, 62, 76, 79, 86, 91, 94, 117, 120, 125, 142, 176, 196, 203, 205, 213, 217])
# isoQNR(4, [0, 3, 4, 19, 21, 23, 56, 62, 76, 79, 86, 91, 94, 117, 120, 125, 142, 176, 196, 203, 205, 213, 217])
print('the singletons are at', singleton_index_list)
print('the lines are at', line_index_list)
print('the polygons are at', poly_index_list)
# impStar(4)

##TODO
# could save gl's, so we can view all quicker
# would seem to be a contradiction between the fact that the 2 imploding has a singleton, the isolated has nothing, but their union is an ellipse. Maybe the arguement of unions doesn't apply so well because we're taking NR(Q^TLQ), not just NR(L)
####TESTING ON N=3 for lines#######
# where is the line from 0 to n? -> 2 exploding, undescribed
# for n = 3
# lines are at [0, 2, 3, 6, 8, 10, 13, 15]
# empty (gn 0), connected exploding (gn 13), fc (gn 15) is point
# 1 exploding(gn 2), 2 cycle (gn 3), is [0,2]
# complex line [-2.5i to 2.5i] (gn 6)
# 2 exploding (gn 8), undescribed (FC minus di-edge) (gn 10) is [1 to n(3)]

# We expected the [0,n] lines to come from (gn3), which is the two exploding star
# plus an isolated vertex, but this is only 0 to 2. It is also a cycle.
#

# g = [[ 0  0  0  0],
# [ 0  0  0  0],
# [-1 -1  3 -1],
# [-1 -1 -1  3]]
########TESTING ON N=4 for lines#######
# for n = 4
# lines are at [0, 3, 4, 19, 21, 23, 56, 62, 76, 79, 86, 91, 94, 117, 120, 125, 142, 176, 196, 203, 205, 213, 217]
# the lines we are looking for are at
# gn 21, which is 2 exploding
# gn 86, which is undescribed? 0 imploded upon, 3 exploding, 1 and 2 exploding
# gn 91, FC(3) + exploding(1).
# gn 94, flux capacitor full flow: exploding(1) spider?
# gn 142, FC(3) + 2cycle
# gn 196, imploding(2) + 2cycle on imploders
# gn 203, diedge four cycle
# gn 205, fc - diedge
# list of lines from [0,n] = 21
# list of lines from [1, n] = [3, 86, 91, 94, 142]
# [2,n] = 196, 203, 205
# [0,n-1] = [23, 56, 62, 79, 117]
# [0,n-2] = [4,19, 120]
# [.5, 3.5] = [125]

[4, 21, 86, 91, 94, 142, 196, 203, 205]

##parameterize the x and y in the complex plane by t,
# solve for t from x, then check to see if that t gives the
# correct y

# line from point a = (a_1,a_2) to b = (b_1,b_2) is c = (a_1,a_2) - t(b_1 - a1, b2 - a2)

# save the eigenvectors associated with polygons for alex
# L1 = np.asarray([
#     [1, 0, 0, 0, -1],
#     [0, 1, 0, 0, -1],
#     [0, 0, 1, 0, -1],
#     [0, 0, 0, 1, -1],
#     [-1, -1, -1, -1, 4]])
# L2 = np.asarray([[2, - 1, 0, -1, 0],
#                  [-1, 2, -1, 0, 0],
#                  [0, -1, 2, -1, 0],
#                  [-1, 0, -1, 2, 0],
#                  [0, 0, 0, 0, 0]])
# print('graph 1')
# nr(L1, 1, True)
# print('graph 2')
# nr(L2, 2, True)


# problem with graph 208 on four vertices, the point is (2,0) but roundoff causes it to have a matrix of
# rank 2
# 208 also seems highly unstable, and the straight line kind of belies what's actually going on
# nearly all the values in the numerical range sampling are at the eignvalues, not between them.
# which is ironic, because most of the area is in the middle

# changed tol to e -14 to protect, changed it to e -13 just to be safe