# Polygonal Graphs
#
# This module determines graphs with polygonal numerical range
#
# Author: Thomas R. Cameron
# Date: 11/24/2019
import itertools
import numpy as np
import networkx as nx
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning)
from math import pi as pi
from matplotlib import pyplot as plt
import sys

EPS = np.finfo(float).eps
graph_num = 1
title = ""
verbose = False


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
def checkHull(convHull, x, y):
    tol = 1000 * EPS
    r0 = convHull[-1]
    res = False
    for k in range(len(convHull)):
        r1 = convHull[k]
        a0 = [r1[0] - r0[0], r1[1] - r0[1]]
        a1 = [x - r0[0], y - r0[1]]
        if (np.linalg.norm(a0) <= tol):
            res = res or (np.linalg.norm(a1) <= tol)
        else:
            a = np.zeros((2, 2))
            a[:, 0] = a0;
            a[:, 1] = a1
            s = np.linalg.svd(a, compute_uv=False)
            res = res or (s[1] < tol * s[0])
        r0 = r1
    return res


###############################################
###             Is Singleton                ###
###############################################
def is_singleton(f):
    """
    checks to see if the shape described by the points in the array
    are really all the same point
    """
    return np.var(f) < 0.001


###############################################
###             Is Singleton                ###
###############################################
def is_line(f):
    """
    checks if the shape described by the points is a real line
    """
    return np.sum(np.absolute(np.imag(f))) < .0000001


###############################################
###             Is Polygon                  ###
###############################################
def isPolygon(f, e):
    edges = []
    for eig in e:
        edges.append((eig.real, eig.imag))
    convHull = convex_hull(edges)
    res = True
    for z in f:
        res = res and checkHull(convHull, z.real, z.imag)
    return res


###############################################
###             Numerical Range             ###
###############################################
def nr(a):
    nv = 360
    n, _ = a.shape
    f = []
    for k in range(1, nv + 1):
        z = np.exp(2 * pi * 1j * (k - 1) / nv)
        a1 = z * a
        a2 = (a1 + np.transpose(np.conjugate(a1))) / 2
        w, v = np.linalg.eig(a2)
        ind = np.argsort(w)
        w = w[ind]
        v = v[:, ind]
        v = v[:, n - 1]
        val = np.dot(np.conjugate(v), np.dot(a, v)) / np.dot(np.conjugate(v), v)

        # kill the roundoff
        if 0 < abs(val.real) < EPS * 10:
            val = val - val.real
        if 0 < abs(val.imag) < EPS * 10:
            val = val - val.imag * 1j

        f.append(val)
    f.append(f[0])
    f = np.array(f)
    evals = np.around(np.linalg.eigvals(a), decimals=13)
    # for eval in evals:
    #     print(type(eval))
    #     if 0 < abs(eval.real) < EPS * 100:
    #         eval = eval - eval.real
    #         eval = 0 + 0j + eval.imag
    #     if 0 < abs(eval.imag) < EPS * 100:
    #         eval = eval - eval.imag * 1j
    #         eval = eval.real + 0j
    return f, evals


###############################################
###             Plot Numerical Range        ###
###############################################
def pltNR(a):
    f, e = nr(a)
    plt.plot(np.real(f), np.imag(f))
    plt.plot(np.real(e), np.imag(e), 'r*')
    # plt.title("Graph Number %d" % graph_num)
    # plt.title(title + "Graph Number %d" % graph_num)
    plt.show()


###############################################
###             Q Numerical Range           ###
###############################################
def qnr(l):
    n, _ = l.shape
    q = np.zeros((n, n - 1))
    for j in range(n - 1):
        q[0:j + 1, j] = 1
        q[j + 1, j] = -(j + 1)
        q[:, j] = q[:, j] / np.linalg.norm(q[:, j])
    a = np.dot(np.transpose(q), np.dot(l, q))
    if verbose:
        print("******** Q Matrix {} ********".format(graph_num))
        print(a)
    # plot Q matrix
    # plt.subplot(224)
    # plt.matshow(a, fignum=False, cmap='winter')
    for i in range(n):
        for j in range(n):
            c = l[j, i]
            plt.text(i, j, str(c), va='center', ha='center', color='white')

    global title
    if abs(np.linalg.norm(a.transpose() @ a - a @ a.transpose(), 'fro')) <= \
            np.linalg.norm(a, 'fro') * sys.float_info.epsilon * 100:
        title = title + ' N_Q '
    elif verbose:
        print('Q normal measure off by', np.linalg.norm(a.transpose() @ a - a
                                                        @ a.transpose(), 'fro'))
        print('and tol was {}'.format(np.linalg.norm(a, 'fro') * 10 * \
                                      sys.float_info.epsilon))
    return nr(a)


###############################################
###             Plot Q Numerical Range      ###
###############################################
def pltQNR(l):
    f, e = qnr(l)
    f_l, e_l = nr(l)
    plt.subplot(223)
    plt.title('NR(Q)')
    plt.plot(np.real(f), np.imag(f))
    plt.plot(np.real(e), np.imag(e), 'g*')
    plt.subplot(224)
    plt.title('NR(L)')
    plt.plot(np.real(f_l), np.imag(f_l))
    plt.plot(np.real(e_l), np.imag(e_l), 'g*')
    return f, e, f_l, e_l


############################################################
###             Unique Permutation                       ###
############################################################
def unique_perm(a):
    ind = range(a.shape[0])
    perm = []
    for i in itertools.permutations(ind):  # all the permutations of [1...n]
        b = a[i, :]
        b = b[:, i]
        add = not any(np.array_equal(b, x) for x in perm)  # finds all the different
        # permutations of b, in a really inefficent way
        if (add):
            perm.append(b)
    return perm


##############################################
###             Poly Graphs
#
# Used to find the polygraphs###
###############################################
def polyGraphs(n):
    mfile = open('matrices/adj' + str(n) + '.txt', 'w+')  # write to this
    adj = []
    adj1 = []
    count = 0
    for i in itertools.product([0, 1], repeat=n * n):
        a = np.reshape(np.array(i), (n, n))
        if (np.trace(a) == 0):
            x = np.array([np.sum(a[i, :]) for i in range(n)])
            d = np.diag(x)
            l = d - a
            f, e, f_l, e_l = qnr(l)  # qnr returns the NR as f and the ev of l as e

            if (isPolygon(f, e)):
                g = nx.DiGraph(a)
                perm = unique_perm(a)  # unique perm returns a whole list of the possible permutations of a
                add = not any(np.array_equal(p, y) for p in perm for y in adj)
                add1 = not any(nx.is_isomorphic(g, y) for y in adj)
                # if add != add1:
                #     print('well fuck')
                assert not (add != add1), 'ya fucked up'  ##logical not xor
                ## perm has all the equiv matrix permutations of a. If any of them are already
                ## in adj, the unique set, then don't add a.
                ## we can improve this by checking for isomorphisms by using the networkx method,
                ## instead of just permuting a on our own and then comparing every permutation
                ## to everything in adj.
                # use https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.isomorphism.is_isomorphic.html#networkx.algorithms.isomorphism.is_isomorphic
                ## to take an adjacency matrix of a directed graph, and check if it's isomorphic
                ## to any of the graphs in adj.
                ## will need to have a constructor to make an object of typ
                # if (add):
                #     adj.append(a)
                #     count = count + 1
                #     print(count)
                if (add1):
                    adj1.append(g)
                    count = count + 1
                    print(count)
    for g in adj:
        for i in range(n):
            for j in range(n - 1):
                mfile.write("%d " % g[i, j])
            mfile.write("%d\n" % g[i, n - 1])
        mfile.write("\n")
    mfile.close()


###############################################
###     display Poly Graphs from non-isomorphic  ###
###############################################
def dispPolyGraphs(n, pt=-1):
    start_time = time.time()
    # mfile = open('matrices/adj' + str(n) + '_pt' + str(pt) + '_cleaned.txt')
    if pt != -1:
        mfile = open('matrices/directed_adjacency_mats/adj' + str(n) + '_pt' + str(pt)+ '.txt')
    else:
        mfile = open('matrices/directed_adjacency_mats/adj' + str(n) + '.txt')
    # if n == 6:
    #     mfile = open('matrices/adj6_first100.txt')
    outfile = open('matrices/poly_adjs/poly_adj' + str(n) + '.txt', 'w+')
    lineList = mfile.readlines()
    a = np.zeros((n, n))
    i = 0
    poly_count = 0
    line_count = 0
    singleton_count = 0
    poly_adj = []
    for row in lineList:
        row = row.split(" ")
        if (len(row) < n or row[0] == 'G'):
            global graph_num
            global title
            title = ""
            g = nx.DiGraph(a)
            nx.draw_shell(g, with_labels=True, ax=plt.subplot(221))

            x = np.array([np.sum(a[i, :]) for i in range(n)])
            l = np.diag(x) - a
            if verbose:
                print("******** Graph Laplacian {} ********".format(graph_num))
                print(l)
            if np.linalg.norm(l.transpose() @ l - l
                              @ l.transpose(), 'fro') == 0:
                title = title + ' N_L '
            elif verbose:
                print('L normal measure off by', np.linalg.norm(l.transpose() @ l - l
                                                                @ l.transpose(), 'fro'))
                print('and tol was 0')
            plt.subplot(221)
            if pt != -1:
                plt.title(title + "Graph Number %d.%d" % (pt, graph_num))
            else:
                plt.title(title + "Graph Number %d" % graph_num)
            plt.subplot(222)
            plt.matshow(l, fignum=False, cmap='winter')


            # write the numbers in the entries

            for k in range(n):
                for j in range(n):
                    c = l[j, k]
                    plt.text(k, j, str(c), va='center', ha='center', color='white')
            f, e = pltQNR(l)
            fig = plt.gcf()
            if is_singleton(f):
                fig.savefig("%d_all/singletonGraph%d/singletonGraph%d.png" % (n, n, graph_num), dpi=400)
                singleton_count += 1
                poly_adj.append(l)
            elif is_line(f):
                fig.savefig("%d_all/lineGraph%d/lineGraph%d.png" % (n, n, graph_num), dpi=400)
                line_count += 1
                poly_adj.append(l)
            elif isPolygon(f, e):
                poly_count += 1
                poly_adj.append(l)
                # plt.show()
                fig.savefig("%d_all/polyGraph%d/polyGraph%d.png" % (n, n, graph_num), dpi=400)
            else:
                fig.savefig("%d_all/other/graph%d.png" % (n, graph_num), dpi = 400)

            plt.clf()
            a = np.zeros((n, n))
            i = 0
            graph_num = graph_num + 1
            if graph_num % 1000 == 0:
                print('Examined graph {}.{}'.format(pt, graph_num))
                print('We have {} singletons, {} lines, and {} polygons'.format(singleton_count,
                                                                    line_count, poly_count))
                print('Total time elapsed ---- %.1f hours' % ((time.time() - start_time) / 3600))

        else:
            a[i, :] = [eval(row[j]) for j in range(n)]
            i = i + 1
    for g in poly_adj:
        for i in range(n):
            for j in range(n - 1):
                outfile.write("%d " % g[i, j])
            outfile.write("%d\n" % g[i, n - 1])
        outfile.write("\n")
    outfile.close()
    return poly_count


###############################################
###             main                        ###
###############################################
#   test polygonal graph methods
###############################################

def main():
    # polyGraphs(3)
    # num_poly_6 = dispPolyGraphs(6, int(sys.argv[1]))
    # print(num_poly_6, 'true polygons')
    dispPolyGraphs(4)
    # dispPolyGraphs(5)


if __name__ == '__main__':
    main()
