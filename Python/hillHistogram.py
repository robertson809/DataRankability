# RM: Hillside Histogram
#
# This module contains functions to study the histogram produced by hillside rankability
#
# Author: Thomas R. Cameron
# Date: 11/18/2019
import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
###############################################
###             hillR                       ###
###############################################
#   Computes Hillside Rankability Measure using brute force approach.
###############################################
def hillR(a):
    """Computes Hillside Rankability Measure using brute force method."""
    # build c matrix from data matrix a 
    n = len(a)
    c = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            c[i,j] = (np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int)))
    # compute kstar, kworst, and p using brute force method
    fitness = []
    perm = list(itertools.permutations(range(n)))
    for k in range(len(perm)):
        temp = c[perm[k],:]
        temp = temp[:,perm[k]]
        temp = temp*np.triu(np.ones((n,n)))
        fitness.append(np.sum(temp))
    # minimum and maximum number of hillside violations
    kstar=np.amin(fitness);
    kworst=np.amax(fitness);
    # histogram plot
    num_bins = (kworst-kstar+1).astype(int);
    values, bins, patches = plt.hist(fitness,bins=num_bins,histtype='bar',ec='black',alpha=0.5)
    # number of rankings with kstar violations
    p = np.sum(np.abs(fitness-kstar)<np.finfo(float).eps)
    # return rankability measures
    return kstar, p, (kworst-kstar)/(kworst+kstar)
###############################################
###             main                        ###
###############################################
#   main method tests rankability measures on big east data
###############################################
def main():
    for year in [1998,2001,2007]:
        # open game file
        f = open('../data_files/CFB/Big East/'+str(year)+'games.txt');
        # read lines
        lineList = f.readlines();
        # store team and score info
        numGames = len(lineList)
        teami = []; scorei = []; teamj = []; scorej = []
        for k in range(numGames):
            row = lineList.pop(0)
            row = row.split(",")
            teami.append(eval(row[2]))
            scorei.append(eval(row[4]))
            teamj.append(eval(row[5]))
            scorej.append(eval(row[7]))
        # create data matrix
        numTeams = max(max(teami),max(teamj))
        d = np.zeros((numTeams,numTeams));
        games = np.zeros((numTeams,numTeams));
        for k in range(numGames):
            # index
            i = teami[k] - 1
            j = teamj[k] - 1
            # record game
            games[i,j] = games[i,j] + 1
            games[j,i] = games[j,i] + 1
            # record win-loss
            if(scorei[k]>scorej[k]):
                d[i,j] = d[i,j] + 1
            else:
                d[j,i] = d[j,i] + 1
        # normalize data matrix
        for i in range(numTeams):
            for j in range(numTeams):
                if(games[i,j]>0):
                    d[i,j] = d[i,j]/games[i,j]
        # close game file
        f.close()
        # create hillside Histogram
        k,p,r = hillR(d)
    # save histogram
    plt.title("Big East 1998, 2001, and 2007")
    plt.savefig("figures/hillHist_BigEast1998-2001-2007.png",dpi=400)
    plt.clf()
    plt.close()
if __name__ == '__main__':
    main()