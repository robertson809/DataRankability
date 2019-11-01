# CFB-Rank-EloCorr: College Football Rankability and Elo Rating Correlation

#
# Author: Thomas R. Cameron
# Date: 10/13/2019
from rm_module import specR, hillR
from copy import deepcopy
import numpy as np

#####################################################
#                 Round by Round Elo Rating         #
#####################################################
def RoundElo(conf,year,eloC1,eloC2):
    # open file
    f = open('../data_files/CFB/'+conf+'/'+str(year)+'games.txt')
    # read all lines
    lineList = f.readlines()
    # store team, score, and date info
    numGames = len(lineList)
    teami = []; scorei = []; teamj = []; scorej = []
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        teami.append(eval(row[2]))
        scorei.append(eval(row[4]))
        teamj.append(eval(row[5]))
        scorej.append(eval(row[7]))
    # close file
    f.close()
    # determine round structure
    numTeams = max(max(teami),max(teamj))
    games_played = [0 for k in range(numTeams)]
    e_row = 0; s_row = 0; k = 0
    count = 1; rnd = []
    while(count<=(numTeams-1)):
        i = teami[k] - 1
        j = teamj[k] - 1
        games_played[i] = games_played[i] + 1
        games_played[j] = games_played[j] + 1
        if(min(games_played)==count):
            e_row = k
            rnd.append([s_row,e_row])
            s_row = e_row + 1
            count = count + 1
        k = k + 1
    # elo rating vector
    numRounds = len(rnd)
    eloRating = np.zeros(numTeams)
    # populate elo rating
    for k in range(numRounds):
        s_row = rnd[k][0]
        e_row = rnd[k][1]
        for l in range(s_row,e_row+1):
            i = teami[l] - 1
            j = teamj[l] - 1
            if(scorei[l]>scorej[l]):
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(1.-u)
                eloRating[j] = eloRating[j] + eloC1*(u-1.)
            elif(scorei[l]<scorej[l]):
                d = eloRating[j] - eloRating[i]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[j] = eloRating[j] + eloC1*(1.-u)
                eloRating[i] = eloRating[i] + eloC1*(u-1.)
            else:
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(0.5-u)
                eloRating[j] = eloRating[j] + eloC1*(u-0.5)
    # return elo rating
    return eloRating
#####################################################
#                 RoundRankability                  #   
#####################################################
def RoundRankability(conf,year):
    # open file
    f = open('../data_files/CFB/'+conf+'/'+str(year)+'games.txt')
    # read all lines
    lineList = f.readlines()
    # store team, score, and date info
    numGames = len(lineList)
    teami = []; scorei = []; teamj = []; scorej = []
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        teami.append(eval(row[2]))
        scorei.append(eval(row[4]))
        teamj.append(eval(row[5]))
        scorej.append(eval(row[7]))
    # close file
    f.close()
    # determine round structure
    numTeams = max(max(teami),max(teamj))
    games_played = [0 for k in range(numTeams)]
    e_row = 0; s_row = 0; k = 0
    count = 1; rnd = []
    while(count<=(numTeams-1)):
        i = teami[k] - 1
        j = teamj[k] - 1
        games_played[i] = games_played[i] + 1
        games_played[j] = games_played[j] + 1
        if(min(games_played)==count):
            e_row = k
            rnd.append([s_row,e_row])
            s_row = e_row + 1
            count = count + 1
        k = k + 1
    # games matrix and rankability vectors
    numRounds = len(rnd)
    games = np.zeros((numTeams,numTeams))
    sr = np.zeros(numRounds)
    hr = np.zeros(numRounds)
    # populate games, sr, and hr
    for k in range(numRounds):
        s_row = rnd[k][0]
        e_row = rnd[k][1]
        for l in range(s_row,e_row+1):
            i = teami[l] - 1
            j = teamj[l] - 1
            if(scorei[l]>scorej[l]):
                games[i,j] = games[i,j] + 1
            elif(scorei[l]<scorej[l]):
                games[j,i] = games[j,i] + 1
            else:
                games[i,j] = games[i,j] + 0.5
                games[j,i] = games[j,i] + 0.5
        # build adjacency matrix
        a = np.zeros((numTeams,numTeams))
        for i in range(numTeams):
            for j in range(i+1,numTeams):
                total = games[i,j] + games[j,i]
                if(total > 0):
                    a[i,j] = games[i,j]/total
                    a[j,i] = games[j,i]/total
        # measure rankability
        sr[k] = specR(a)
        hr[k] = hillR(a)
    # return rankability measures
    return sr, hr
#####################################################
#                 Main                              #
#####################################################
def Main():
    # open files
    f1 = open('csv/CFB-Rank-EloCorr-Rounds.csv','w+')
    f2 = open('csv/CFB-Rank-EloCorr-Summary.csv','w+')
    # file header
    f1.write('Conference, Year, Round, specR, hillR\n')
    f2.write('Conference, Year, specR, hillR, EloCorrCoef\n')
    ### Big East ###
    eloCorr = []
    srank = []
    hrank = []
    for year in range(1995,2013):
        sr, hr = RoundRankability('Big East',year)
        srank.append(sr[-1])
        hrank.append(hr[-1])
        for k in range(len(sr)):
            f1.write('Big East, '+str(year)+', '+str(k+1)+', '+str(sr[k])+', '+str(hr[k])+'\n')
        x = []
        for k in range(20,45):
            for l in range(400,1601,50):
                e = RoundElo('Big East',year,k,l)
                x.append(e)
        eloCorr.append(np.amin(np.corrcoef(x)))
        f2.write('Big East, '+str(year)+', '+str(sr[-1])+', '+str(hr[-1])+', '+str(eloCorr[-1])+'\n')
    # close files
    f1.close()
    f2.close()
    # print correlation 
    print(np.corrcoef([eloCorr,srank,hrank]))
    
# call Main       
Main()