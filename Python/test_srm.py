# TEST_SRM: Test the Spectral Rankability Measure module. 
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import specR, connR
import numpy as np

#####################################################
#                 Adjacency Matrices                #
#####################################################

#nam = ['Dominance Graph','Dominance+Perturbation','Perturbed Random Graph','Nearly Disconnected','Random','Cyclic','Completely Connected','Empty Graph']

#adj = [np.array([[0.,1,1,1,1,1],[0,0.,1,0,1,1],[0,0,0.,0,1,1],[0,1,1,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
#        np.array([[0.,1,1,1,1,1],[0,0.,0,1,1,1],[1,0,0.,1,1,1],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0]]),
#        np.array([[0.,1,0,0,1,1],[0,0.,1,1,0,0],[0,1,0.,0,0,0],[1,0,0,0.,0,1],[0,0,0,1,0.,0],[1,1,1,0,1,0.]]),
#        np.array([[0.,1,1,1,0,0],[0,0.,1,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
#        np.array([[0.,1,0,0,0,1],[0,0.,1,1,0,0],[0,1,0.,0,0,0],[1,0,0,0.,0,1],[0,0,0,0,0.,0],[0,1,1,0,0,0.]]),
#        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,0],[0,0,0.,1,0,0],[0,0,0,0.,1,0],[0,0,0,0,0.,1],[1,0,0,0,0,0.]]),
#        np.array([[0.,1,1,1,1,1],[1,0.,1,1,1,1],[1,1,0.,1,1,1],[1,1,1,0.,1,1],[1,1,1,1,0.,1],[1,1,1,1,1,0.]]),
#        np.zeros((6,6))
#        ]
        
#####################################################
#                 Test Rankability Measure          #
#####################################################
#for k in range(len(nam)):
#    print(nam[k]+':')
#    print('rankH = '+str('%.3f' % rankH(adj[k]))+' and rankM = '+str('%.3f' % rankM(adj[k])))

#####################################################
#                 Big East D1 NCAA Football         #
#####################################################
years = [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012]
for k in range(len(years)):
    print('Year'+str(years[k])+': ')
    f = open('../data_files/Big_East_Football/matrices/binaryMatrix'+str(years[k])+'.txt')
    lineList = f.readlines()
    n = len(lineList)
    a = np.zeros((n,n))
    for i in range(n):
        row = lineList.pop(0)
        row = row.split("   ")
        for j in range(1,n+1):
            a[i][j-1] = row[j]
    print('specR = '+str('%.3f' % specR(a))+' and connR = '+str('%.3f' % connR(a)))

#print('\n')
#####################################################
#                 NCAA_D1_matrices                  #
#####################################################
#years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012]
#for k in range(len(years)):
#    print('Year'+str(years[k])+': ')
#    f = open('../data_files/NCAA_D1_matrices/binaryMatrix'+str(years[k])+'.txt')
#    lineList = f.readlines()
#    n = len(lineList)
#    a = np.zeros((n,n))
#    for i in range(n):
#        row = lineList.pop(0)
#        row = row.split("   ")
#        for j in range(1,n+1):
#            a[i][j-1] = row[j]
#    print('rankH = '+str('%.3f' % rankH(a))+' and rankA = '+str('%.3f' % rankA(a))+' rankA+rankH = '+str('%.3f' % (rankA(a)+rankH(a)))+'\n')

#####################################################
#                 Test Rankability Acyclic Graphs   #
#####################################################
#adj = [np.array([[0.,1,1,0,0,0],[0,0.,1,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
#        np.array([[0.,1,1,0,0,0],[0,0.,1,1,0,0],[0,0,0.,0,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
#        np.array([[0.,1,1,0,0,0],[0,0.,1,0,0,0],[0,0,0.,1,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]])
#        ]
#for k in range(len(adj)):
#    print('rankH = '+str('%.3f' % rankH(adj[k])))
#    print('rankA = '+str('%.3f' % rankA(adj[k])))