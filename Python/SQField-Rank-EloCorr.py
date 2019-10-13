# SQField-Rank-EloFit: Sinquefield Cup Rankability and Elo Rating Correlation
#
# Author: Thomas R. Cameron
# Date: 10/12/2019
from srm_module import specR
from copy import deepcopy
import numpy as np

#####################################################
#                 Round by Round Analysis           #
#####################################################
def RoundAnalysis(year,eloC1,eloC2):
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
    # games matrix, elo rating and rankability vectors
    games = np.zeros((numPlayers,numPlayers))
    eloRating = np.zeros(numPlayers)
    rankability = np.zeros(numRounds)
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
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(1.-u)
                eloRating[j] = eloRating[j] + eloC1*(u-1.)
            elif(row[1]<0):
                games[j,i] = games[j,i] + 1
                d = eloRating[j] - eloRating[i]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[j] = eloRating[j] + eloC1*(1.-u)
                eloRating[i] = eloRating[i] + eloC1*(u-1.)
            else:
                games[i,j] = games[i,j] + 0.5
                games[j,i] = games[j,i] + 0.5
                d = eloRating[i] - eloRating[j]
                u = 1./(1.+10.**(-d/eloC2))
                eloRating[i] = eloRating[i] + eloC1*(0.5-u)
                eloRating[j] = eloRating[j] + eloC1*(u-0.5)
        a = np.zeros((numPlayers,numPlayers))
        for i in range(numPlayers):
            for j in range(i+1,numPlayers):
                total = games[i,j] + games[j,i]
                if(total > 0):
                    a[i,j] = games[i,j]/total
                    a[j,i] = games[j,i]/total
        rankability[k] = specR(a)
    return rankability,eloRating

#####################################################
#                 Main                              #
#####################################################
def Main():
    corr = np.zeros(7)
    rank = np.zeros(7)
    for year in range(2013,2020):
        x = []
        for k in range(20,60):
            for l in range(380,420):
                r, e = RoundAnalysis(year,k,l)
                x.append(e)
        corr[year-2013] = np.amin(np.corrcoef(x))
        rank[year-2013] = r[-1]
        
    print(corr)
    print(rank)
    print(np.corrcoef([corr,rank]))
    
# call Main       
Main()