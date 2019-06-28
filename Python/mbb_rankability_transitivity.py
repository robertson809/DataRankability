# MBB_Rankability_Transitivity: Rankability Measures for the entire MBB, with the added assumption of transitivity for teams that did not originally play.
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
        i = teami[k] - 1
        j = teamj[k] - 1
        if(scorei[k]>scorej[k]):
            games[i,j] = games[i,j] + 1
        else:
            games[j,i] = games[j,i] + 1
    # create adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    for i in range(numTeams):
        for j in range(i+1,numTeams):
            total = games[i,j] + games[j,i]
            if(total!=0):
                adj[i,j] = games[i,j]/total
                adj[j,i] = games[j,i]/total
    # transitivity assumption
    for i in range(numTeams):
        for j in range(numTeams):
            if(adj[i,j]==1):
                for k in range(numTeams):
                    if(adj[j,k]==1 and adj[i,k]==0 and adj[k,i]==0):
                        adj[i,k]=1
    # return adjacency matrix
    return adj
    
#####################################################
#                 Main                              #
#####################################################
def main():
    # open file
    f = open("mbb_rankability_transitivity.csv","w+")
    f.write('Year, specR, sparsity \n')
    years = [(2002+k) for k in range(17)]
    for k in range(len(years)):
        adj = read_data(years[k])
        f.write(str('%d' % years[k])+str(',%.15f' % specR(adj))+str(',%.15f' % sparsity(adj))+'\n')
        
        
main()
#read_data(2001)