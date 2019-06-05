# MBB_Mountain_West: Rankability Measures for MBB Mountain West Conference
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import rankA, rankB, specR, connR
import numpy as np

years = [2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]

#####################################################
#                 Read Data Matrix                  #
#####################################################
def read_data_matrix(year):
    f = open('../data_files/ConferencesMBB/Mountain_West/binaryMatrix'+str(year)+'.txt')
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
#                alpha_beta                         #
#####################################################
def alpha_beta():
    f = open("mbb_mountain_west_alphabeta.csv","w+")
    f.write('Year, alpha, beta \n')
    alge_rank = [0 for i in range(len(years))]
    beta_rank = [0 for i in range(len(years))]
    for k in range(len(years)):
        a = read_data_matrix(years[k])
        alge_rank[k] = rankA(a)
        beta_rank[k] = rankB(a)
    m = max(alge_rank)
    alge_rank = [alge_rank[i]/m for i in range(len(years))]
    m = max(beta_rank)
    beta_rank = [beta_rank[i]/m for i in range(len(years))]
    for k in range(len(years)):
        print('Year'+str(years[k])+': ')
        f.write(str('%d' % years[k])+str(', %.15f' % alge_rank[k])+str(', %.15f' % beta_rank[k])+'\n')
        #print('alphaR = '+str('%.3f' % alge_rank[k])+' and betaR = '+str('%.3f' % beta_rank[k])+'\n')
    f.close()
        
#####################################################
#                Rankability                        #
#####################################################
def rankability():
    f = open("mbb_mountain_west_rankability.csv","w+")
    f.write('Year, specR, connR \n')
    for k in range(len(years)):
        print('Year'+str(years[k])+': ')
        a = read_data_matrix(years[k])
        f.write(str('%d' % years[k])+str(', %.15f' % specR(a))+str(', %.15f' % connR(a))+'\n')
        #print('specR = '+str('%.3f' % specR(a))+' and connR = '+str('%.3f' % connR(a))+'\n')
    f.close()
   
alpha_beta()
rankability()