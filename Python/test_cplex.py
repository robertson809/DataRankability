#!/usr/bin/python
# ---------------------------------------------------------------------------
# File: test_cplex.py
# Version 1.0
# ---------------------------------------------------------------------------
# Test CPLEX using python and barrier LP solver
# ---------------------------------------------------------------------------
import cplex
import numpy as np
from copy import deepcopy
#from cplex.exceptions import CplexSolverError


def perm(r,indI,indJ):
    if(len(indI)==0):
        return [r]
        
    lst = []
    for p in perm(r,indI[1:],indJ[1:]):
        lst.append(deepcopy(p))
        temp = p[indI[0]]
        p[indI[0]] = p[indJ[0]]
        p[indJ[0]] = temp
        lst.append(deepcopy(p))
            
    return lst

# tolerance
TOL = 1e-6
EPS = np.finfo(float).eps
# problem description
obj = [0.0,2.0,3.0,2.0,0.0,3.0,0.0,0.0,0.0]
lb = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
ub = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
colnames = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
rhs = [1.0,1.0,1.0,2.0,2.0]
rownames = ["c1", "c2", "c3", "c4", "c5"]
sense = "EEELL"
# build and solve problem
prob = cplex.Cplex()
#prob.set_log_stream(None)
#prob.set_error_stream(None)
#prob.set_warning_stream(None)
prob.set_results_stream(None)
prob.objective.set_sense(prob.objective.sense.minimize)
prob.linear_constraints.add(rhs=rhs, senses=sense, names=rownames)
prob.variables.add(obj=obj, lb=lb, ub=ub, names=colnames)
rows = [0,0,1,1,2,2,3,3,3,4,4,4]
cols = [1,3,2,6,5,7,1,5,6,2,3,7]
vals = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
alg = prob.parameters.lpmethod.values
prob.parameters.lpmethod.set(alg.barrier)
prob.parameters.barrier.crossover.set(prob.parameters.barrier.crossover.values.none)
prob.solve()
#print("Solution status = ", prob.solution.get_status(), ":", end=' ')
#print(prob.solution.status[prob.solution.get_status()])
#print("Solution value  = ", prob.solution.get_objective_value())
x = prob.solution.get_values()

# hill side rankability k values
n = 3
x = np.array(x)
x[x<TOL] = 0.0
kstar = np.dot(x,obj)
x = x.reshape((n,n))
obj = np.array(obj).reshape((n,n))
r = list(np.sum(x,axis=1).argsort()) # ascending order (worst ranking)
c = obj[r,:]
c = c[:,r]
kworst = np.sum(c*np.triu(np.ones((n,n))))
print("kstar = %.2f" % kstar)
print("kworst = %.2f" % kworst)

# hill side rankability p set
r = r[::-1] # descending order (best ranking)
permX = x[r,:]
permX = permX[:,r]
indI = []
indJ = []
for i in range(n):
    for j in range(n):
        if(permX[i,j]<1 and permX[i,j]>0):
            if(i not in indJ):
                indI.append(i)
                indJ.append(j)

print(indI)
print(indJ)
pList = perm(r,indI,indJ)
temp = []
for r in pList:
    c = obj[r,:]
    c = c[:,r]
    if(np.abs(np.sum(c*np.triu(np.ones((n,n)))) - kstar)<EPS):
        temp.append(r)

pList = temp
print(pList)
#pSet = set([])
#for k in range(len(indI)):
#    ranking = deepcopy(r)
#    ranking[indI[k]], ranking[indJ[k]] = ranking[indJ[k]], ranking[indI[k]]
#    print(ranking)
#    pSet.add(tuple(ranking))