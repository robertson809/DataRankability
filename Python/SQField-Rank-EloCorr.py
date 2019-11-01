# SQField-Rank-EloCorr: Sinquefield Cup Rankability and Elo Rating Correlation
#
# Author: Thomas R. Cameron
# Date: 10/12/2019
from rm_module import specR, hillR_BF, hillR_LP
import numpy as np

#####################################################
#                 Round by Round Elo Rating         #
#####################################################
def RoundElo(year,eloC1,eloC2):
    # open file
    f = open('../data_files/SinquefieldCup/SinquefieldCup'+str(year)+'.csv')
    # read all lines
    lineList = f.readlines()
    # grab first line and split
    row = lineList.pop(0)
    row = row.split(",")
    # store numPlayers and numRounds
    numPlayers = eval(row[0])
    numRounds = eval(row[1])
    # elo rating vector
    eloRating = np.zeros(numPlayers)
    # populate elo rating
    for k in range(numRounds):
        for l in range(numPlayers//2):
            row = lineList.pop(0)
            row = row.split(",")
            row = [eval(row[m]) for m in range(len(row))]
            i = row[0]-1
            j = row[2]-1
            if(row[1]>0):
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(1.-u)
                eloRating[j] = eloRating[j] + eloC1*(u-1.)
            elif(row[1]<0):
                d = eloRating[j] - eloRating[i]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[j] = eloRating[j] + eloC1*(1.-u)
                eloRating[i] = eloRating[i] + eloC1*(u-1.)
            else:
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(0.5-u)
                eloRating[j] = eloRating[j] + eloC1*(u-0.5)
    return eloRating
#####################################################
#                 RoundRankability                  #   
#####################################################
def RoundRankability(year):
    # open file
    f = open('../data_files/SinquefieldCup/SinquefieldCup'+str(year)+'.csv')
    # read all lines
    lineList = f.readlines()
    # grab first line and split
    row = lineList.pop(0)
    row = row.split(",")
    # store numPlayers and numRounds
    numPlayers = eval(row[0])
    numRounds = eval(row[1])
    # games matrix and rankability vectors
    games = np.zeros((numPlayers,numPlayers))
    sr = np.zeros(numRounds)
    hr = np.zeros(numRounds)
    # populate games, eloRating, rankability
    for k in range(numRounds):
        for l in range(numPlayers//2):
            row = lineList.pop(0)
            row = row.split(",")
            row = [eval(row[m]) for m in range(len(row))]
            i = row[0]-1
            j = row[2]-1
            if(row[1]>0):
                games[i,j] = games[i,j] + 1
            elif(row[1]<0):
                games[j,i] = games[j,i] + 1
            else:
                games[i,j] = games[i,j] + 0.5
                games[j,i] = games[j,i] + 0.5
        # build adjacency matrix
        a = np.zeros((numPlayers,numPlayers))
        for i in range(numPlayers):
            for j in range(i+1,numPlayers):
                total = games[i,j] + games[j,i]
                if(total > 0):
                    a[i,j] = games[i,j]/total
                    a[j,i] = games[j,i]/total
        # measure rankability
        sr[k] = specR(a)
        hr[k] = hillR_LP(a)
        #hr[k] = hillR_BF(a)
    return sr, hr
#####################################################
#                 Main                              #
#####################################################
def Main():
    eloCorr = []
    srank = []
    hrank = []
    for year in range(2013,2020):
        sr, hr = RoundRankability(year)
        srank.append(sr[-1])
        hrank.append(hr[-1])
        x = []
        for k in range(30,51):
            for l in range(300,501,10):
                e = RoundElo(year,k,l)
                x.append(e)
        eloCorr.append(np.amin(np.corrcoef(x)))
        
    print(eloCorr)
    print(srank)
    print(hrank)
    print(np.corrcoef([eloCorr,srank,hrank]))
    
# call Main       
Main()