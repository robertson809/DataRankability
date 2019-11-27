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
                    # print('point {} on line {}'.format(count, i))
                    on_line = True
                    break
                # else:
                #     print('not on line ', i)
        if not on_line:
            return False
    print('is a polygon')
    return True


# def allQNR(n, r_graph_num=-1, disp=False):
#     """
#     Finds and prints ALL the restricted numerical ranges of graphs on n vertices. Does not consider uniqueness
#     around isomorphism
#     :param n: the number of vertices
#     :param r_graph_num: potential to specify a graph or list of graphs rather than all graphs, default -1
#                         prints all graphs
#     :param disp: the option to display pictures of the graphs generated
#     :return:
#     """
#     adj = []
#     # produces a list of flattened matrices with 1,0 entries
#     for i in itertools.product([0, 1], repeat=n * n):
#         a = np.reshape(np.array(i), (n, n))  # don't give a shit if this is unique or not
#         if np.trace(a) == 0:
#             adj.append(a)
#
#     if r_graph_num != -1:  # turn adj into a singleton or shortened list
#         if type(r_graph_num) == int:
#             g = adj[r_graph_num]
#             adj = [g]
#         if type(r_graph_num) == list:
#             adj = [adj[num] for num in r_graph_num]
#
#     graph_num = 0
#     for a in adj:
#         x = np.array([np.sum(a[i, :]) for i in range(n)])
#         l = np.diag(x) - a
#         if disp:
#             if r_graph_num == -1:
#                 plt.title('Graph {}'.format(graph_num))
#             elif type(r_graph_num) == int:
#                 plt.title('Graph {}'.format(r_graph_num))
#             elif type(r_graph_num) == list:
#                 plt.title('Graph {}'.format(r_graph_num[graph_num]))
#             g = nx.DiGraph(a)
#             nx.draw(g, with_labels=True, ax=plt.subplot(121))
#         graph_num += 1
#         qnr(l, graph_num, disp)


def all_qnr(n, r_graph_num=-1, disp=True, check_iso=True):
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
            if not check_iso:
                adj.append(a)
                continue
            add = not any(np.array_equal(p, x) for p in perm for x in adj)
            if add:
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
pseduocycles = [27, 0]
lines = [21]
three_IS = [0, 6, 13, 15]
four_IS = [0, 76, 176, 213, 217]

all_qnr(4, r_graph_num=82, disp=True)
print('the singletons are at', singleton_index_list)
print('the lines are at', line_index_list)
print('the polygons are at', poly_index_list)

#  [4, 21, 86, 91, 94, 142, 196, 203, 205]

# problem with graph 208 on four vertices, the point is (2,0) but roundoff causes it to have a matrix of
# rank 2
# 208 also seems highly unstable, and the straight line kind of belies what's actually going on
# nearly all the values in the numerical range sampling are at the eignvalues, not between them.
# which is ironic, because most of the area is in the middle

# changed tol to e -14 to protect, changed it to e -13 just to be safe