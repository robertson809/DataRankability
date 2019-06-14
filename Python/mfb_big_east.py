# Big_East_Football: Rankability Measures for MFB Big East Conference
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
    f = open('../data_files/Big_East_Football/'+str(year)+'games.txt')
    # number of teams
    if(1995<=year<=2003 or 2005<=year<=2012):
        numTeams = 8
    elif(year==2004):
        numTeams = 7
    # initialize adjacency matrix
    adj = np.zeros((numTeams,numTeams))
    # read lines
    lineList = f.readlines()
    # number of games
    numGames = len(lineList)
    # record dominance
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        i = eval(row[2]) - 1
        j = eval(row[5]) - 1
        scorei = eval(row[4])
        scorej = eval(row[7])
        if(scorei>scorej):
            adj[i,j] = 1
        else:
            adj[j,i] =  1
    # return
    return adj
    
#####################################################
#                 Main                              #
#####################################################
def main():
    f = open("mfb_big_east_rankability.csv","w+")
    f.write('Year, specR \n')
    years = [(1995+k) for k in range(18)]
    for k in range(len(years)):
        adj = read_data_specR(years[k])
        f.write(str('%d' % years[k])+str(',%.15f' % specR(adj))+'\n')
    
main()