# MBB_Conference_Rankability: Rankability Analysis for MBB conferences
#
# Author: Thomas R. Cameron
# Date: 8/13/2019
from srm_module import specR
import numpy as np

#####################################################
#                 Read Data                         # 
#####################################################
def read_data(conf,year):
    # open games file
    f = open('../data_files/MBB/conference/'+conf+'/'+str(year)+'games.txt')
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
    wins = np.zeros((numTeams,numTeams))
    for k in range(numGames):
        ii = teami[k] - 1
        jj = teamj[k] - 1
        if(scorei[k]>scorej[k]):
            wins[ii,jj] = wins[ii,jj] + 1
        else:
            wins[jj,ii] = wins[jj,ii] + 1
    # create adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    for ii in range(numTeams):
        for jj in range(ii+1,numTeams):
            total = wins[ii,jj] + wins[jj,ii]
            if(total!=0):
                adj[ii,jj] = wins[ii,jj]/total
                adj[jj,ii] = wins[jj,ii]/total
    # return adjacency matrix
    return adj
    
#####################################################
#                 Main                              #
#####################################################
def main():
    # open file
    f = open("csv/MBB_Conf_Rank.csv","w+")
    # store conferences
    conferences = ['America East','Atlantic 10','Atlantic Coast','Atlantic Sun','Big 10','Big 12','Big East', \
                    'Big Sky','Big South','Big West','Colonial','Conference USA','Horizon','Ivy League', \
                    'Metro Atlantic','Mid-American','Mid-Eastern AC','Missouri Val','Northeast','OH Valley', \
                    'Patriot League','Southeastern','Southern','Southland','Southwestern AC','Sun Belt','West Coast']
    # write conferences in first row of file
    for k in range(len(conferences)):
        f.write(','+conferences[k])
    f.write('\n')
    # store years
    years = [(2002+k) for k in range(18)]
    # for each year, compute rankability of all conferences
    for i in range(len(years)):
        f.write(str('%d'%years[i]))
        for j in range(len(conferences)):
            adj = read_data(conferences[j],years[i])
            f.write(',%.15f' % specR(adj))
        f.write('\n')
    
#########################
#       Call Main       #
#########################
main()