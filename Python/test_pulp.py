# TEST_PULP: Test Pulp for solving LP problem
#
# Author: Thomas R. Cameron
# Date: 10/15/2019
import numpy as np
import pulp

# problem class
my_lp_problem = pulp.LpProblem("My LP Problem",pulp.LpMaximize)
# decision variables
x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
print(my_lp_problem)
# objective function
#my_lp_problem += 4*x + 3*y, "z"
# constraints 
#my_lp_problem += 2*y <= 25 - x
#my_lp_problem += 4*y >= 2*x - 8
#my_lp_problem += y <= 2*x - 5
# print problem
#print(my_lp_problem)
# solve problem
#my_lp_problem.solve()
#pulp.LpStatus[my_lp_problem.status]
# check variables
#for var in my_lp_problem.variables():
#    print(var.name + " = "+str(var.varValue))
# optimal value
#print("z = "+str(pulp.value(my_lp_problem.objective)))

# c matrix
#n = 5
#c = np.array([[0,0,0,0,0],[2,0,0,0,0],[4,2,0,0,0],[6,4,2,0,0],[8,6,4,2,0]],dtype=float)
# problem class
#rank_lp_problem = pulp.LpProblem("Hillside Rankability",pulp.LpMinimize)
# decision variables
#x = [[pulp.LpVariable("x{0}_{1}".format(i,j),lowBound=0,upBound=1,cat='Continuous') for j in range(n)] for i in range(n)]
# objective function
#obj = np.sum(c*x)
#rank_lp_problem += obj, "z"
# constraints
#for i in range(n):
#    for j in range(i+1,n):
#            rank_lp_problem += x[i][j] + x[j][i] == 1
#for i in range(n):
#    for j in range(n):
#        for k in range(n):
#            if(j!=i and k!=j and k!=i):
#                rank_lp_problem += x[i][j] + x[j][k] + x[k][i] <= 2
# print problem
#print(rank_lp_problem)
# solve problem
#rank_lp_problem.solve()
#pulp.LpStatus[rank_lp_problem.status]
# check variables
#x = np.zeros((n,n))
#for var in rank_lp_problem.variables():
#    x[int(var.name[1]),int(var.name[3])] = var.varValue
#print(x)
# optimal value
#print("z = "+str(pulp.value(rank_lp_problem.objective)))