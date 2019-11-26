# RM: Rankability Measure
#
# This module contains the functions for edgeR, hillR, and specR
#
# Author: Thomas R. Cameron
# Date: 11/13/2019
import itertools
from math import factorial
import numpy as np
from scipy.stats import spearmanr
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
    s = np.array([n-k for k in range(1,n+1)])
    # eigenvalues of given graph Laplacian
    e = np.linalg.eigvals(l)
    # rankability measure
    return 1. - ((Hausdorff(e,s)+Hausdorff(x,s))/(2*(n-1)))
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
            c[i,j] = -(np.count_nonzero((a[:,j]<a[:,i]).astype(int)) + np.count_nonzero((a[i,:]<a[j,:]).astype(int)))
    # compute kstar, kworst, and p using brute force method
    fitness = []
    perm = list(itertools.permutations(range(n)))
    for k in range(len(perm)):
        temp = c[perm[k],:]
        temp = temp[:,perm[k]]
        temp = temp*np.triu(np.ones((n,n)))
        fitness.append(-np.sum(temp))
    # minimum and maximum number of hillside violations
    kstar=np.amin(fitness);
    kworst=np.amax(fitness);
    # number of rankings with kstar violations
    p = np.sum(np.abs(fitness-kstar)<np.finfo(float).eps)
    # return rankability measures
    return kstar, p, (kworst-kstar)/(kworst+kstar)
###############################################
###             edgeR                       ###
###############################################
#   Computes edge Rankability Measure using brute force approach.
###############################################
def edgeR(a):
    # size
    n = len(a)
    # complete dominance
    domMat = np.triu(1.0*np.ones((n,n)),1)
    # fitness list
    fitness = []
    # brute force (consider all permutations)
    for i in itertools.permutations(range(n)):
        b = a[i,:]
        b = b[:,i]
        # number of edge changes (k) for given permutation
        fitness.append(np.sum(np.abs(domMat - b)))
    # minimum and maximum number of edge chagnes
    kstar = np.amin(fitness)
    kworst = np.amax(fitness)
    # number of permutations that give kstar
    p = np.sum(np.abs(fitness-kstar)<np.finfo(float).eps)
    # return rankability measures
    return kstar, p, (kworst-kstar)/(kworst+kstar)
###############################################
###             main                        ###
###############################################
#   main method tests rankability measures on big east data
###############################################
def main():
    # rankability lists
    ek = []; ep = []; hk = []; hp = []
    er = []; hr = []; sr = []
    # results file
    fr = open('csv/simod2.csv','w+')
    fr.write('Year, Anderson [k p r], Hillside [k p r], specR\n')
    for year in range(1995,2013):
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
        # compute and write rankability measures
        fr.write('%d,' % year)
        k, p, r = edgeR(d)
        ek.append(k); ep.append(p); er.append(r)
        fr.write('[%.4f %.4f %.4f],' % (k,p,r))
        k, p, r = hillR(d)
        hk.append(k); hp.append(p); hr.append(r)
        fr.write('[%.4f %.4f %.4f],' % (k,p,r))
        r = specR(d)
        sr.append(r)
        fr.write('%.4f\n' % r)
        # close game file
        f.close()
    # close results file
    fr.close()
    # print correlation measures
    corr,pval = spearmanr(ek,hk);
    print('Anderson k and Hillside k corr = %.4f' % corr)
    print('Anderson k and Hillside k pval = %.4f' % pval)
    corr,pval = spearmanr(ep,hp);
    print('Anderson p and Hillside p corr = %.4f' % corr)
    print('Anderson p and Hillside p pval = %.4f' % pval)
    corr,pval = spearmanr(er,hr);
    print('Anderson r and Hillside r corr = %.4f' % corr)
    print('Anderson r and Hillside r pval = %.4f' % pval)
    corr,pval = spearmanr(er,sr);
    print('Anderson r and specR corr = %.4f' % corr)
    print('Anderson r and specR pval = %.4f' % pval)
    corr,pval = spearmanr(hr,sr);
    print('Hillside r and specR corr = %.4f' % corr)
    print('Hillside r and specR pval = %.4f' % pval)
if __name__ == '__main__':
    main()