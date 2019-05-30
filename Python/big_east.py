# BIG_EAST: Rankability Measures for Big East Data
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import rankA, rankB, specR, connR, ranking
import numpy as np

years = [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012]

#####################################################
#                 Read Data Matrix                  #
#####################################################
def read_data_matrix(year):
    f = open('../data_files/Big_East/matrices/binaryMatrix'+str(year)+'.txt')
    lineList = f.readlines()
    n = len(lineList)
    a = np.zeros((n,n))
    for i in range(n):
        row = lineList.pop(0)
        row = row.split("   ")
        for j in range(1,n+1):
            a[i][j-1] = row[j]
    return a
            
#####################################################
#                Rankability                        #
#####################################################
def rankability():
    spec_rank = [0 for i in range(len(years))]
    alge_rank = [0 for i in range(len(years))]
    beta_rank = [0 for i in range(len(years))]
    for k in range(len(years)):
        a = read_data_matrix(years[k])
        spec_rank[k] = specR(a)
        alge_rank[k] = rankA(a)
        beta_rank[k] = rankB(a)
    m = max(alge_rank)
    alge_rank = [alge_rank[i]/m for i in range(len(years))]
    m = max(beta_rank)
    beta_rank = [beta_rank[i]/m for i in range(len(years))]
    for k in range(len(years)):
        print('Year'+str(years[k])+': ')
        print('specR = '+str('%.3f' % spec_rank[k])+' and alphaR = '+str('%.3f' % alge_rank[k])+' and betaR = '+str('%.3f' % beta_rank[k])+'\n')
        
#####################################################
#                Rankability New                    #
#####################################################
def rankability_new():
    for k in range(len(years)):
        print('Year'+str(years[k])+': ')
        a = read_data_matrix(years[k])
        print('specR = '+str('%.3f' % specR(a))+' and connR = '+str('%.3f' % connR(a))+'\n')
        
#####################################################
#                Ranking                            #
#####################################################
def ranking():
    print('Year 2000:')
    a = read_data_matrix(years[5])
    print('ranking = '+str(ranking(a))+'\n')
    print('Year 2001:')
    a = read_data_matrix(years[6])
    print('ranking = '+str(ranking(a))+'\n')
   
rankability()
#rankability_new()
#ranking()