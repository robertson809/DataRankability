# SQField-Rank-EloFit: Rankability Measures for Sinquefield Cup and Comparison to the Elo rating fit
#
# Author: Thomas R. Cameron
# Date: 6/21/2019
from srm_module import specR
from copy import deepcopy
import numpy as np

# Elo constant
K = 40.
H = 5.
X = 400.

#####################################################
#                 Ranking Fit                       #
#####################################################
def Ranking_Fit(r1,r2):
    # indices that would sort array in ascending order
    ind1 = np.argsort(r1)
    ind2 = np.argsort(r2)
    # store number of changes in ranking
    numChanges = 0
    for k in range(len(ind1)):
        if(ind1[k]!=ind2[k]):
            numChanges = numChanges + 1
    # return
    return  1. - float(numChanges)/float(len(ind1))

#####################################################
#                 Read Data                         #
#####################################################
def Read_Data(year):
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
    # create games, adj, and r lists
    games = [np.zeros((numPlayers,numPlayers)) for k in range(numRounds)]
    adj = [np.zeros((numPlayers,numPlayers)) for k in range(numRounds)]
    elo_rating = [np.zeros(numPlayers) for k in range(numRounds)]
    forw_pred = [0 for k in range(numRounds)]
    # populate games, adj, and r lists
    for k in range(numRounds):
        # copy previous rounds game info
        games[k] = deepcopy(games[k-1])
        # copy previous rounds elo_rating info
        elo_rating[k] = deepcopy(elo_rating[k-1])
        # update game info
        for l in range(numPlayers//2):
            row = lineList.pop(0)
            row = row.split(",")
            row = [eval(row[m]) for m in range(len(row))]
            i = row[0]-1
            j = row[2]-1
            # copy of Elo rating
         #   x = deepcopy(elo_rating[k-1])
            if(row[1]>0):
                # player i beat player j
                games[k][i,j] = games[k][i,j] + 1
                # forw_pred
                if(elo_rating[k][i]>(elo_rating[k][j]+H)):
                    forw_pred[k] = forw_pred[k] + 1
                # update player i Elo rating
                d = elo_rating[k][i] - elo_rating[k][j]
                u = 1./(1.+10.**(-d/X))
                elo_rating[k][i] = elo_rating[k][i] + K*(1.-u)
         #       x[i] = x[i] + K*(1.-u)
                # update player j Elo rating
                elo_rating[k][j] = elo_rating[k][j] + K*(u-1.)
         #       x[j] = x[j] + K*(u-1.)
            elif(row[1]<0):
                # player j beat player i
                games[k][j,i] = games[k][j,i] + 1
                # forw_pred
                if(elo_rating[k][j]>(elo_rating[k][i]+H)):
                    forw_pred[k] = forw_pred[k] + 1
                # update player j Elo rating
                d = elo_rating[k][j] - elo_rating[k][i]
                u = 1./(1.+10.**(-d/X))
                elo_rating[k][j] = elo_rating[k][j] + K*(1.-u)
         #       x[j] = x[j] + K*(1.-u)
                # update player i Elo rating
                elo_rating[k][i] = elo_rating[k][i] + K*(u-1.)
         #       x[i] = x[i] + K*(u-1.)
            else:
                # draw
                games[k][i,j] = games[k][i,j] + 0.5
                games[k][j,i] = games[k][j,i] + 0.5
                # forw_pred
                if(abs(elo_rating[k][i]-elo_rating[k][j])<=H):
                    forw_pred[k] = forw_pred[k] + 1
                # update player i Elo rating
                d = elo_rating[k][i] - elo_rating[k][j]
                u = 1./(1.+10.**(-d/X))
                elo_rating[k][i] = elo_rating[k][i] + K*(0.5-u)
         #       x[i] = x[i] + K*(0.5-u)
                # update player j Elo rating
                elo_rating[k][j] = elo_rating[k][j] + K*(u-0.5)
         #       x[j] = x[j] + K*(u-0.5)
            # record predictability
         #   if(abs(Ranking_Fit(x,elo_rating[k-1])-1.)<np.finfo(float).eps):
         #       forw_pred[k] = forw_pred[k] + 1
        # update adjacency matrix
        for i in range(numPlayers):
            for j in range(numPlayers):
                total = games[k][i,j] + games[k][j,i]
                if(total>1):
                    # player i and j played twice
                    adj[k][i,j] = games[k][i,j]/2
                elif(total>0):
                    # player i and j played once
                    adj[k][i,j] = games[k][i,j]
                # otherwise, player i and j did not play
    # return
    return adj, elo_rating, forw_pred, numPlayers, numRounds
    
#####################################################
#                 Backward Predictability           #
#####################################################
def Back_Pred(year,elo_rating):
    # open file
    f = open('../data_files/SinquefieldCup/SinquefieldCup'+str(year)+'.csv')
    # read all lines
    lineList = f.readlines()
    # remove header info
    lineList.pop(0)
    # compute back_pred
    numGames = len(lineList)
    back_pred = 0
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        row = [eval(row[m]) for m in range(len(row))]
        i = row[0]-1
        j = row[2]-1
       # x = deepcopy(elo_rating)
        if(row[1]>0):
            if(elo_rating[i]>(elo_rating[j]+H)):
                back_pred = back_pred + 1
    #        d = x[i] - x[j]
    #        u = 1./(1.+10.**(-d/X))
    #        x[i] = x[i] + K*(1.-u)
    #        x[j] = x[j] + K*(u-1.)
        elif(row[1]<0):
            if(elo_rating[j]>(elo_rating[i]+H)):
                back_pred = back_pred + 1
    #        d = x[j] - x[i]
    #        u = 1./(1.+10.**(-d/X))
    #        x[j] = x[j] + K*(1.-u)
    #        x[i] = x[i] + K*(u-1.)
        else:
            if(abs(elo_rating[i]-elo_rating[j])<=H):
                back_pred = back_pred + 1
    #        d = x[i] - x[j]
    #        u = 1./(1.+10.**(-d/X))
    #        x[i] = x[i] + K*(1.-u)
    #        x[j] = x[j] + K*(u-1.)
        # record predictability
    #    if(abs(Ranking_Fit(x,elo_rating)-1.)<np.finfo(float).eps):
    #        back_pred = back_pred + 1
    # close file
    f.close()
    # return
    return float(back_pred)/float(numGames)
    
#####################################################
#                 Main                              #
#####################################################
def Main():
    # open files
    f1 = open('csv/SQField-Rank-EloFit-Rounds.csv','w+')
    f2 = open('csv/SQField-Rank-EloFit-Summary.csv','w+')
    # round by round analysis and summary
    f1.write('Year, Round, Rank, Forw_Pred \n')
    f2.write('Year, Rank, Forw_Pred, Back_Pred \n')
    x = []; y = []; z = []
    for year in range(2013,2019):
        adj, elo_rating, forw_pred, numPlayers, numRounds = Read_Data(year)
        f1.write('%d,,,\n' % year)
        for k in range(numRounds):
            f1.write(',%d,%.4f,%.4f\n' % (k+1,specR(adj[k]),forw_pred[k]/(numPlayers/2.)))
        x.append(specR(adj[-1]))
        y.append(sum(forw_pred[1:numRounds])/(numRounds*(numPlayers/2.)))
        z.append(Back_Pred(year,elo_rating[-1]))
        f2.write(',%.4f,%.4f,%.4f\n' % (x[-1],y[-1],z[-1]))
    # correlation between year summary data
    print('\tforw_pred corr = %.4f' % np.corrcoef(x,y)[0,1])
    print('\tback_pred corr = %.4f' % np.corrcoef(x,z)[0,1])
    # close files
    f1.close()
    f2.close()
    # for each year get adjacency matrix and ranking info
    #for year in range(2013,2019):
    #    adj, elo_rating, pred = read_data(year)
    #    f.write(str('%d' % year)+',,,'+'\n')
    #    # for each round write rankability and ranking fit to file
    #    for rd in range(len(adj)):
    #        if(rd==0):
    #            f.write(','+str('%d' % (rd+1))+str(',%.4f' % specR(adj[rd]))+str(',%.4f' % 0)+'\n')
    #        else:
    #            f.write(','+str('%d' % (rd+1))+str(',%.4f' % specR(adj[rd]))+str(',%.4f' % RankingFit(elo_rating[rd-1],elo_rating[rd]))+'\n')
    # close file
    #f.close()
    # print correlation between fit and rankability
    #x = []
    #y = []
    #z = []
    #for year in range(2013,2019):
    #    adj, elo_rating, pred = Read_Data(year)
    #    numRounds = len(adj)
    #    x.append(specR(adj[numRounds-1]))
    #    y.append(Ranking_Fit(elo_rating[numRounds-2],elo_rating[numRounds-1]))
    #    z.append(pred)
    #print(np.corrcoef(x,y))
    #print(np.corrcoef(x,z))
            

# call Main       
Main()