# MBB_West_Coast: Rankability Measures for MBB West Coast Conference
#
# Author: Thomas R. Cameron
# Date: 6/14/2019
from srm_module import specR, spec2R
import numpy as np

#####################################################
#                 Read Data for specR               #
#####################################################
def read_data_specR(year):
    # open games file
    f = open('../data_files/ConferencesMBB/West_Coast/'+str(year)+'games.txt')
    # number of teams
    if(2002<=year<=2011):
        numTeams = 8
        confGames = 7
    elif(2012<=year<=2013):
        numTeams = 9
        confGames = 8
    elif(2014<=year<=2019):
        numTeams = 10
        if(year==2016):
            confGames = 8
        else:
            confGames = 9
    # initialize adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    # read lines
    lineList = f.readlines()
    # number of games
    numGames = len(lineList) - confGames
    # record dominance
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        i = eval(row[2]) - 1
        j = eval(row[5]) - 1
        scorei = eval(row[4])
        scorej = eval(row[7])
        if(scorei>scorej):
            if(adj[j,i]==1):
                adj[i,j] = 0.5
                adj[j,i] = 0.5
            else:
                adj[i,j] = 1
        else:
            if(adj[i,j]==1):
                adj[j,i] = 0.5
                adj[i,j] = 0.5
            else:
                adj[j,i] =  1
    # return
    return adj

#####################################################
#                 Read Data for spec2R              #
#####################################################
def read_data_spec2R(year):
    # open games file
    f = open('../data_files/ConferencesMBB/West_Coast/'+str(year)+'games.txt')
    # number of teams
    if(2002<=year<=2011):
        numTeams = 8
        confGames = 7
    elif(2012<=year<=2013):
        numTeams = 9
        confGames = 8
    elif(2014<=year<=2019):
        numTeams = 10
        if(year==2016):
            confGames = 8
        else:
            confGames = 9
    # initialize adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    # read lines
    lineList = f.readlines()
    # number of games
    numGames = len(lineList) - confGames
    # record games
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        i = eval(row[2]) - 1
        j = eval(row[5]) - 1
        scorei = eval(row[4])
        scorej = eval(row[7])
        if(scorei>scorej):
            adj[i,j] = adj[i,j] + 1
        else:
            adj[j,i] = adj[j,i] + 1
    # return
    return adj
    
#####################################################
#                 Main                              #
#####################################################
def main():
    f = open("mbb_west_coast_rankability.csv","w+")
    f.write('Year, specR, spec2R \n')
    years = [(2002+k) for k in range(18)]
    for k in range(len(years)):
        adj1 = read_data_specR(years[k])
        adj2 = read_data_spec2R(years[k])
        f.write(str('%d' % years[k])+str(',%.15f' % specR(adj1))+str(',%.15f' % spec2R(adj2))+'\n')
    
main()