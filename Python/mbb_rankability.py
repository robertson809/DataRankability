# MBB_Rankability: Rankability Measures for the entire MBB.
#
# Author: Thomas R. Cameron
# Date: 6/15/2019
from srm_module import specR, spec2R
import numpy as np

#####################################################
#                 sparsity                          # 
#####################################################
def sparsity(a):
    m = a.shape[0]
    n = a.shape[1]
    c = 0
    for i in range(m):
        for j in range(n):
            if(a[i,j]!=0):
                c = c + 1
    return(float(c)/float(m*n))

#####################################################
#                 Read Data                         # 
#####################################################
def read_data(year):
    # open games file
    f = open('../data_files/AllMBB-Verbos/'+str(year)+'games.txt')
    # read lines
    lineList = f.readlines()
    # store info
    numGames = len(lineList)
    teami = []
    scorei = []
    teamj = []
    scorej = []
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        teami.append(eval(row[2]))
        scorei.append(eval(row[4]))
        teamj.append(eval(row[5]))
        scorej.append(eval(row[7]))
    # create games matrix
    numTeams = max(max(teami),max(teamj))
    games = np.zeros((numTeams,numTeams))
    for k in range(numGames):
        ii = teami[k] - 1
        jj = teamj[k] - 1
        if(scorei[k]>scorej[k]):
            games[ii,jj] = games[ii,jj] + 1
        else:
            games[jj,ii] = games[jj,ii] + 1
    # create adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    for ii in range(numTeams):
        for jj in range(ii+1,numTeams):
            total = games[ii,jj] + games[jj,ii]
            if(total!=0):
                adj[ii,jj] = games[ii,jj]/total
                adj[jj,ii] = games[jj,ii]/total
    # return adjacency matrix
    return adj
    
#####################################################
#                 Main                              #
#####################################################
def main():
    # open file
    f = open("mbb_rankability.csv","w+")
    f.write('Year, specR, sparsity \n')
    years = [(2002+k) for k in range(17)]
    for k in range(len(years)):
        adj = read_data(years[k])
        f.write(str('%d' % years[k])+str(',%.15f' % specR(adj))+str(',%.15f' % sparsity(adj))+'\n')
        
        
main()