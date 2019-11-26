# RM: Rankability Measure
#
# This module contains the functions for Hillside Rankability measure and Spectral Rankability measure.
#
# Author: Thomas R. Cameron
# Date: 10/13/2019
import itertools
from math import factorial
import cplex
import numpy as np
from copy import deepcopy

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
###             hillR_BF                    ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
def hillR_BF(a):
    """Computes Hillside Rankability Measure using brute force method."""
    # build c matrix from data matrix a 
    n = len(a)
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = -(np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int)))
    # compute kstar, kworst, and p using brute force method
    fitness = []
    perm = list(itertools.permutations(range(n)))
    for k in range(len(perm)):
        temp = c[perm[k],:]
        temp = temp[:,perm[k]]
        temp = temp*np.triu(np.ones((n,n)))
        fitness.append(-np.sum(temp))
    kstar=np.amin(fitness);
    kworst=np.amax(fitness);
    #p = sum((fitness==kstar).astype(int))
    # compute rankability
    if(kstar==0 and kworst==0):
        return 0.
    else:
        #return 1. - kstar*p/(kworst*factorial(n))
        return (kworst-kstar)/(kworst+kstar)

###############################################
###             hillR_LP                    ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
def hillR_LP(a):
    """Computes Hillside Rankability Measure by solving LP using CPLEX."""
    # paramters
    TOL = 1e-6
    EPS = np.finfo(float).eps
    # perm function
    def _perm(r,indI,indJ):
        if(len(indI)==0):
            return [r]
        
        lst = []
        for p in _perm(r,indI[1:],indJ[1:]):
            lst.append(deepcopy(p))
            temp = p[indI[0]]
            p[indI[0]] = p[indJ[0]]
            p[indJ[0]] = temp
            lst.append(deepcopy(p))
            
        return lst
    # build c matrix from data matrix a 
    n = len(a)
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int))
    # objective function and bounds
    obj = c.reshape(n*n)
    lb = np.zeros(n*n)
    ub = np.ones(n*n)
    colnames = ["x"+str(i) for i in range(n*n)]
    rownames = ["c"+str(i) for i in range(n*(n-1)//2 + n*(n-1)*(n-2))]
    # equality constraints
    count = 0; sense = ""
    rows = []; cols = []; vals = []; rhs = []
    for i in range(n-1):
        for j in range(i+1,n):
            rows.extend([count,count]);
            cols.append(n*i+j); cols.append(n*j+i)
            vals.extend([1.0,1.0])
            rhs.append(1.0)
            sense = sense + "E"
            count = count + 1
    # inequality constraints
    tcol = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if(j!=i and k!=j and k!=i):
                    tset = {n*i+j,n*j+k,n*k+i}
                    if(tset not in tcol):
                        tcol.append(tset)
                        rows.extend([count,count,count])
                        vals.extend([1.0,1.0,1.0])
                        rhs.append(2.0)
                        sense = sense + "L"
                        count = count + 1
                        for s in tset:
                            cols.append(s)
    # colnames and rownames
    colnames = ["x"+str(i) for i in range(n*n)]
    rownames = ["c"+str(i) for i in range(count)]
    # cplex problem variable
    prob = cplex.Cplex()
    # quite results
    prob.set_results_stream(None)
    # minimization problem
    prob.objective.set_sense(prob.objective.sense.minimize)
    # problem variables
    prob.variables.add(obj=obj, lb=lb, ub=ub, names=colnames)
    # linear constraints
    prob.linear_constraints.add(rhs=rhs, senses=sense, names=rownames)
    prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
    # barrier method
    alg = prob.parameters.lpmethod.values
    prob.parameters.lpmethod.set(alg.barrier)
    prob.parameters.barrier.crossover.set(prob.parameters.barrier.crossover.values.none)
    # solve problem
    prob.solve()
    # solution status
    print("Hillside LP Solution Status = ", prob.solution.get_status(), ":", end=' ')
    print(prob.solution.status[prob.solution.get_status()])
    # store solution values
    x = prob.solution.get_values()
    x = np.array(x)
    x[x<TOL] = 0.0
    x[(1-x)<TOL] = 1.0
    # kstar
    kstar = np.dot(x,obj)
    # k worst
    x = x.reshape((n,n))
    obj = np.array(obj).reshape((n,n))
    r = list(np.sum(x,axis=1).argsort()) # ascending order (worst ranking)
    c = obj[r,:]
    c = c[:,r]
    kworst = np.sum(c*np.triu(np.ones((n,n))))
    print("kstar = %.2f" % kstar)
    print("kworst = %.2f" % kworst)
    # pSet
    r = r[::-1] # descending order (best ranking)
    permX = x[r,:]
    permX = permX[:,r]
    indI = []
    indJ = []
    for i in range(n):
        for j in range(i+1,n):
            if(permX[i,j]<1 and permX[i,j]>0):
                indI.append(i)
                indJ.append(j)
    print(permX)
    print(indI)
    print(indJ)
    c = obj[r,:]
    c = c[:,r]
    k = np.sum(c*np.triu(np.ones((n,n))))
    pList = _perm(r,indI,indJ)
    temp = []
    for r in pList:
        c = obj[r,:]
        c = c[:,r]
        if(np.abs(np.sum(c*np.triu(np.ones((n,n)))) - kstar)<TOL):
            temp.append(r)
        # testing
        print(r)

    pList = temp
    for p in pList:
        print(p)
###############################################
###             hillR_LP                    ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
#def hillR_LP(a):
#    """Computes Hillside Rankability Measure by solving LP using Pulp."""
#    # build c matrix from data matrix a 
#    n = len(a)
#    c = np.zeros((n,n))
#    for i in range(n):
#        for j in range(n):
#            c[i,j] = np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int))
#    print(c)
#    # hillside rankability pulp class
#    hillLP= pulp.LpProblem("Hillside LP",pulp.LpMinimize)
#    # decision variables
#    x = [[pulp.LpVariable("x{0}_{1}".format(i,j),lowBound=0,upBound=1,cat="Continuous") for j in range(n)] for i in range(n)]
#    # objective function
#    hillLP += np.sum(c*x)
#    # antisymmetry constraint
#    for i in range(n):
#        for j in range(i+1,n):
#                hillLP += x[i][j] + x[j][i] == 1
#    # transitivity constraint
#    for i in range(n):
#        for j in range(n):
#            for k in range(n):
#                if(j!=i and k!=j and k!=i):
#                    hillLP += x[i][j] + x[j][k] + x[k][i] <= 2
#    hillLP.writeLP('hillLP.lp')
#    quit()
#    #print(hillLP)
#    # solve problem
#    hillLP.solve()
#    print("Status:", pulp.LpStatus[hillLP.status])
#    # optimal k value
#    kstar = pulp.value(hillLP.objective)
#    if(kstar==None):
#        return 0.
#    # worst k value
#    x = np.zeros((n,n))
#    for var in hillLP.variables():
#        ind = var.name.find('_')
#        x[int(var.name[1:ind]),int(var.name[ind+1:])] = var.varValue
#    print(kstar)
#    print(x)
#    quit()
#    perm = np.sum(x,axis=1).argsort() # ascending order (worst ranking)
#    permC = c[perm,:]
#    permC = permC[:,perm]
#    kworst = np.sum(permC*np.triu(np.ones((n,n))))
#    # test
#    perm = np.flip(perm)
#    permC = c[perm,:]
#    permC = permC[:,perm]
#    # print kstar and kworst
#    print(kstar)
#    print(kworst)
#    # call hillR_Pset
#    #hillR_Pset(x,kstar)
#    # return rankability
#    if(kstar<TOL and kworst<TOL):
#        return 0.
#    else:
#        return (kworst-kstar)/(kworst+kstar)
###############################################
###             hillR_Pset                  ###
###############################################
#   Computes Hillside Rankability P set.
###############################################
#def hillR_Pset(x,kstar):
#    """Computes Hillside Rankability P set."""
#    perm = np.sum(x,axis=1).argsort()[::-1]
#    permX = x[perm,:]
#    permX = permX[:,perm]
#    print(permX)
        
###############################################
###             hillR_Deprecated            ###
###############################################
#   Computes Hillside Rankability Measure.
###############################################
#def hillR_Deprecated(a):
#    """Computes Hillside Rankability Measure using scipy linprog."""
#    # build c matrix from data matrix a 
#    n = len(a)
#    c = np.zeros((n,n))
#    for i in range(n):
#        for j in range(n):
#            c[i,j] = np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int))
#    # reshape c matrix
#    c = c.reshape(n**2)
#    # create Aeq matrix and beq vector for Yoshi's constraint 1
#    con = 0
#    row = []; col = []; data = []
#    for j in range(n-1):
#        for i in range(j+1,n):
#            row.extend([con,con]); data.extend([1,1])
#            col.append(n*j+i); col.append(n*i+j)
#            con = con + 1
#    Aeq = csc_matrix((data, (row,col)), shape=(n*(n-1)//2,n*n))
#    beq = np.ones(n*(n-1)//2)
#    # create A matrix and b vector for Yoshi's constraint 2
#    con = 0
#    row = []; col = []; data = []
#    for i in range(n):
#        for l in range(n-1):
#            j = list(set(range(n)).difference({i}))
#            for m in range(n-2):
#                k = list(set(range(n)).difference({i,j[m]}))
#                col.append(n*j[l]+i); col.append(n*k[m]+j[l]); col.append(n*i+k[m])
#                row.extend([con,con,con]); data.extend([1,1,1])
#                con = con + 1
#    A = csc_matrix((data, (row,col)), shape=(n*(n-1)*(n-2),n*n))
#    b = 2*np.ones(n*(n-1)*(n-2))
#    # define lb and ub vectors (must be integer type)
#    lb = np.zeros(n*n,dtype=int)
#    ub = np.ones(n*n,dtype=int)
#    # force specific indices to be zero
#    index = list(range(0,n*n,n+1))
#    ub[index] = 0
#    # store bounds
#    bounds = []
#    for k in range(n*n):
#        bounds.append((lb[k],ub[k]))
#    # solve LP relaxation
#    res = linprog(c,A,b,Aeq,beq,bounds=bounds,method='interior-point',options={'sparse':True});
#    # optimal ordering (perm) and reversal (revPerm)
#    x = np.reshape(res.x,(n,n))
#    s = np.sum(x,axis=1)
#    revPerm = s.argsort()
#    perm = revPerm[::-1]
#    # optimal value (kstar) and reversal (kworst)
#    kstar = res.fun
#    c = c.reshape((n,n))
#    revPermC = c[revPerm,:]
#    revPermC = revPermC[:,revPerm]
#    kworst = np.sum(revPermC*np.triu(np.ones((n,n))))
#    # return rankability
#    if(kstar<TOL and kwosrt<TOL):
#        return 0.
#    else:
#        return (kworst-kstar)/(kworst+kstar)