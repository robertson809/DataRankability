# MBB_Conference_Rankability: Rankability Measures for all MBB Conferences
#
# Author: Thomas R. Cameron
# Date: 6/15/2019
from srm_module import specR
import numpy as np

#####################################################
#                 Read Data                         # 
#####################################################
def read_data(conf,year):
    # open games file
    f = open('../data_files/MBB/conference/'+str(conf)+'/'+str(year)+'games.txt')
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
    f = open("csv/mbb_conference_rankability.csv","w+")
    # store conferences
    conferences = ['America East','Atlantic 10','Atlantic Coast','Atlantic Sun','Big 10','Big 12','Big East','Big Sky',
                    'Big South','Big West','Colonial','Conference USA','Horizon',
                    'Ivy League','Metro Atlantic','Mid-American','Mid-Eastern AC','Missouri Val',
                    'Mountain West','Northeast','OH Valley','Patriot League','Southeastern',
                    'Southern','Southland','Southwestern AC','Sun Belt','West Coast']
    # write conferences in first row of file
    for k in range(len(conferences)):
        f.write(','+conferences[k])
    f.write('\n')
    # store years
    years = [(2002+k) for k in range(18)]
    # for all year and all conferences, compute rankability
    for i in range(len(years)):
        f.write(str('%d'%years[i]))
        for j in range(len(conferences)):
            adj = read_data(conferences[j],years[i])
            f.write(str(',%.15f' % specR(adj)))
        f.write('\n')

main()