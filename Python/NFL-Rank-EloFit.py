# NFL-Rank-EloFit: Rankability Measures for NFL conferences and Comparison to the Elo ranking fit
#
# Author: Thomas R. Cameron
# Date: 7/15/2019
from copy import deepcopy
import numpy as np

# Elo constants
K = 40.
H = 5.
X = 400.

###############################################
###             Hausdorff                   ###
###############################################
#   Hausdorff distance between sets e and s.
###############################################
def Hausdorff(e,s):
    """Hausdorff distance between sets e and s."""
    def _sv(e,s):
        return max([min([abs(e[i]-s[j]) for j in range(len(s))]) for i in range(len(e))])
    return max(_sv(e,s),_sv(s,e))
    
###############################################
###             specR                       ###
###############################################
#   Computes Spectral Rankability Measure.
###############################################
def specR(a):
    """Computes Spectral Rankability Measure."""
    # given graph Laplacian
    n = len(a)
    x = np.array([np.sum(a[i,:]) for i in range(n)])
    d = np.diag(x)
    l = d - a;
    # perfect dominance graph spectrum and out-degree
    # s = np.array([n-k for k in range(1,n+1)])
    # eigenvalues of given graph Laplacian
    e = np.linalg.eigvals(l)
    # rankability measure
    # return 1. - ((Hausdorff(e,s)+Hausdorff(x,s))/(2*(n-1)))
    return 1. - (Hausdorff(e,x)/(n-1))

#####################################################
#                 Read Data                         #
#####################################################
def Read_Data(conf,year):
    # open file
    f = open('../data_files/NFL/'+str(conf)+'/'+str(year)+'games.txt')
    # read all lines
    lineList = f.readlines()
    # store team, score, and date info
    numGames = len(lineList)
    date = []; teami = []; scorei = []; teamj = []; scorej = []
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        date.append(eval(row[0]))
        teami.append(eval(row[2]))
        scorei.append(eval(row[4]))
        teamj.append(eval(row[5]))
        scorej.append(eval(row[7]))
    # determine round structure
    numTeams = max(max(teami),max(teamj))
    games_played = [0 for k in range(numTeams)]
    e_row = 0; s_row = 0
    rnd = []
    for k in range(numGames-5):
        i = teami[k] - 1
        j = teamj[k] - 1
        games_played[i] = games_played[i] + 1
        games_played[j] = games_played[j] + 1
        if(date[k+1]>date[k]+3):
            e_row = k
            rnd.append([s_row,e_row])
            s_row = e_row + 1
    # initalize games, adjacency, elo_rating, and forw_pred arrays
    numRounds = len(rnd)
    games = [np.zeros((numTeams,numTeams)) for k in range(numRounds)]
    adj = [np.zeros((numTeams,numTeams)) for k in range(numRounds)]
    elo_rating = [np.zeros(numTeams) for k in range(numRounds)]
    forw_pred = [0 for k in range(numRounds)]
    # store game, adjacency, elo_rating, and forw_pred info round by round
    for k in range(numRounds):
        s_row = rnd[k][0]
        e_row = rnd[k][1]
        # copy over games, win-losses, and Elo rating from (k-1) round
        games[k] = deepcopy(games[k-1])
        adj[k] = deepcopy(adj[k-1])
        elo_rating[k] = deepcopy(elo_rating[k-1])
        # record games and win-losses for kth round
        # also, update Elo rating and forw_pred
        for l in range(s_row,e_row+1):
            # team i and team j
            i = teami[l] - 1
            j = teamj[l] - 1
            # game record
            games[k][i,j] = games[k][i,j] + 1
            games[k][j,i] = games[k][j,i] + 1
            # win-loss record
            if(scorei[l]>scorej[l]):
                # team i > team j
                adj[k][i,j] = adj[k][i,j] + 1
                # forw_pred
                if(elo_rating[k][i]>(elo_rating[k][j]+H)):
                    forw_pred[k] = forw_pred[k] + 1
                # Elo rating
                d = elo_rating[k][i] - elo_rating[k][j]
                u = 1./(1.+10.**(-d/X))
                elo_rating[k][i] = elo_rating[k][i] + K*(1.-u)
                elo_rating[k][j] = elo_rating[k][j] + K*(u-1.)
            else:
                # team j > team i
                adj[k][j,i] = adj[k][j,i] + 1
                # forw_pred
                if(elo_rating[k][i]<(elo_rating[k][j]+H)):
                    forw_pred[k] = forw_pred[k] + 1
                # Elo rating
                d = elo_rating[k][j] - elo_rating[k][j]
                u = 1./(1.+10.**(-d/X))
                elo_rating[k][j] = elo_rating[k][j] + K*(1.-u)
                elo_rating[k][i] = elo_rating[k][i] + K*(u-1.)
    # normalize adjacency array round by round
    for k in range(numRounds):
        for i in range(numTeams):
            for j in range(numTeams):
                if(games[k][i,j]!=0):
                    adj[k][i,j] = adj[k][i,j]/games[k][i,j]
    # close file
    f.close()
    # return
    return adj, elo_rating, forw_pred, rnd
    
#####################################################
#                 Backward Predictability           #
#####################################################
def Back_Pred(conf,year,elo_rating):
    # open file
    f = open('../data_files/NFL/'+str(conf)+'/'+str(year)+'games.txt')
    # read all lines
    lineList = f.readlines()
    # compute back_pred
    numGames = len(lineList)
    back_pred = 0
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        teami = eval(row[2]) - 1
        scorei = eval(row[4])
        teamj = eval(row[5]) - 1
        scorej = eval(row[7])
        if(scorei>scorej):
            if(elo_rating[teami]>(elo_rating[teamj]+H)):
                back_pred = back_pred + 1
        else:
            if(elo_rating[teami]<(elo_rating[teamj]+H)):
                back_pred = back_pred + 1
    # close file
    f.close()
    # return
    return float(back_pred)/float(numGames)
    
#####################################################
#                 Main                              #
#####################################################
def Main():
    # open files
    f1 = open('csv/NFL-Rank-EloFit-Rounds.csv','w+')
    f2 = open('csv/NFL-Rank-EloFit-Summary.csv','w+')
    # rankability and predictability
    rank = []
    forwPred = []
    backPred = []
    
    # AFC
    print('AFC: ')
    x = []; y = []; z = []
    f1.write('AFC,Year,Round,Rank,Forw-Pred\n')
    f2.write('AFC,Year,Rank,Forw-Pred,Back-Pred\n')
    for year in range(2002,2019):
        f1.write(',%d,,,\n' % year)
        f2.write(',%d' % year)
        adj, elo_rating, forw_pred, rnd = Read_Data('afc',year)
        numRounds = len(rnd)
        for k in range(numRounds):
            f1.write(',,%d,%.4f,%.4f\n' % (k+1,specR(adj[k]),forw_pred[k]/float(rnd[k][1]-rnd[k][0]+1)))
        # year summary
        x.append(specR(adj[-1]))
        y.append(sum(forw_pred[1:numRounds])/float(rnd[-1][1]-rnd[0][1]+1))
        z.append(Back_Pred('afc',year,elo_rating[-1]))
        f2.write(',%.4f,%.4f,%.4f\n' % (x[-1],y[-1],z[-1]))
    # correlation between year summary data
    print('\tforw_pred corr = %.4f' % np.corrcoef(x,y)[0,1])
    print('\tback_pred corr = %.4f' % np.corrcoef(x,z)[0,1])
    # update rank, forwPred, and backPred
    rank = rank + x
    forwPred = forwPred + y
    backPred = backPred + z
    
    # NFC
    print('NFC: ')
    x = []; y = []; z = []
    f1.write('NFC,Year,Round,Rank,Forw-Pred\n')
    f2.write('NFC,Year,Rank,Forw-Pred,Back-Pred\n')
    for year in range(2002,2019):
        f1.write(',%d,,,\n' % year)
        f2.write(',%d' % year)
        adj, elo_rating, forw_pred, rnd = Read_Data('nfc',year)
        numRounds = len(rnd)
        for k in range(numRounds):
            f1.write(',,%d,%.4f,%.4f\n' % (k+1,specR(adj[k]),forw_pred[k]/float(rnd[k][1]-rnd[k][0]+1)))
        # year summary
        x.append(specR(adj[-1]))
        y.append(sum(forw_pred[1:numRounds])/float(rnd[-1][1]-rnd[0][1]+1))
        z.append(Back_Pred('nfc',year,elo_rating[-1]))
        f2.write(',%.4f,%.4f,%.4f\n' % (x[-1],y[-1],z[-1]))
    # correlation between year summary data
    print('\tforw_pred corr = %.4f' % np.corrcoef(x,y)[0,1])
    print('\tback_pred corr = %.4f' % np.corrcoef(x,z)[0,1])
    # update rank, forwPred, and backPred
    rank = rank + x
    forwPred = forwPred + y
    backPred = backPred + z

    # close files
    f1.close()
    f2.close()
    
    # complete correlation summary
    print('Complete Summary: ')
    print('\tforw_pred corr = %.4f' % np.corrcoef(rank,forwPred)[0,1])
    print('\tback_pred corr = %.4f' % np.corrcoef(rank,backPred)[0,1])

# call Main
Main()