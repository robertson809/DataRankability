# MBB_MountainWest: Rankability Measures for MBB Mountain West Conference
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
    f = open('../data_files/ConferencesMBB/Mountain_West/'+str(year)+'games.txt')
    # number of teams
    if(2002<=year<=2005 or year==2012):
        numTeams = 8
        confGames = 7
    elif(2006<=year<=2011 or year==2013):
        numTeams = 9
        confGames = 8
    elif(2014<=year<=2019):
        numTeams = 11
        if(year==2015):
            confGames = 9
        else:
            confGames = 10
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
    f = open('../data_files/ConferencesMBB/Mountain_West/'+str(year)+'games.txt')
    # number of teams
    if(2002<=year<=2005 or year==2012):
        numTeams = 8
        confGames = 7
    elif(2006<=year<=2011 or year==2013):
        numTeams = 9
        confGames = 8
    elif(2014<=year<=2019):
        numTeams = 11
        if(year==2015):
            confGames = 9
        else:
            confGames = 10
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
#       Conference Tournament Predictability        #
#####################################################
def CTPred(year):
    if(year==2002):
        pred = 3.0/7.0
    elif(year==2003):
        pred = 3.0/7.0
    elif(year==2004):
        pred = 5.0/7.0
    elif(year==2005):
        pred = 5.0/7.0
    elif(year==2006):
        pred = 5.0/8.0
    elif(year==2007):
        pred = 5.0/8.0
    elif(year==2008):
        pred = 5.0/8.0
    elif(year==2009):
        pred = 5.0/8.0
    elif(year==2010):
        pred = 4.0/8.0
    elif(year==2011):
        pred = 5.0/8.0
    elif(year==2012):
        pred = 6.0/7.0
    elif(year==2013):
        pred = 7.0/8.0
    elif(year==2014):
        pred = 8.0/10.0
    elif(year==2015):
        pred = 6.0/9.0
    elif(year==2016):
        pred = 5.0/10.0
    elif(year==2017):
        pred = 8.0/10.0
    elif(year==2018):
        pred = 6.0/10.0
    elif(year==2019):
        pred = 9.0/10.0
    return pred
    
#####################################################
#                 Main                              #
#####################################################
def main():
    f = open("mbb_mountain_west_rankability.csv","w+")
    f.write('Year, specR, spec2R, CTPred \n')
    years = [(2002+k) for k in range(18)]
    for k in range(len(years)):
        adj1 = read_data_specR(years[k])
        adj2 = read_data_spec2R(years[k])
        f.write(str('%d' % years[k])+str(',%.15f' % specR(adj1))+str(',%.15f' % spec2R(adj2))+str(',%.15f' % CTPred(years[k]))+'\n')
    
main()