# CFB_Conference_Rankability: Rankability Measures for all CFB Conferences
#
# Author: Thomas R. Cameron
# Date: 6/20/2019
from srm_module import specR, matchR
import numpy as np

#####################################################
#                 Read Data                         # 
#####################################################
def read_data(conf,year):
    # open games file
    f = open('../data_files/CFB/'+conf+'/'+str(year)+'games.txt')
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
    f = open("csv/cfb_conference_rankability.csv","w+")
    # store conferences
    conferences = ['Big 12']
    # write conferences in first row of file
    for k in range(len(conferences)):
        f.write(conferences[k]+',,,')
    f.write('\n')
    # store years
    years = [(1996+k) for k in range(23)]
    # for all year and all conferences, compute rankability
    for i in range(len(years)):
        f.write(str(',%d'%years[i]))
        for j in range(len(conferences)):
            adj = read_data(conferences[j],years[i])
            f.write(str(',%.15f' % specR(adj))+str(',%.15f' % specR(adj)))
        f.write('\n')

main()