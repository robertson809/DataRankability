# SinquefieldCup: Rankability Measures for Sinquefield Cup
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import specR, spec2R
from copy import deepcopy
import numpy as np

#####################################################
#                 Read Data                         #
#####################################################
def read_data(year):
    f = open('../data_files/SinquefieldCup/SinquefieldCup'+str(year)+'.csv')
    lineList = f.readlines()
    row = lineList.pop(0)
    row = row.split(",")
    numPlayers = eval(row[0])
    numRounds = eval(row[1])
    adj = [np.zeros((numPlayers,numPlayers)) for k in range(numRounds)]
    for k in range(numRounds):
        adj[k] = deepcopy(adj[k-1])
        for l in range(numPlayers/2):
            row = lineList.pop(0)
            row = row.split(",")
            row = [eval(row[m]) for m in range(len(row))]
            i = row[0]-1
            j = row[2]-1
            if(row[1]>0):
                adj[k][i,j] = adj[k][i,j] + 1
            elif(row[1]<0):
                adj[k][j,i] = adj[k][j,i] + 1 
            else:
                adj[k][i,j] = adj[k][i,j] + 0.5
                adj[k][j,i] = adj[k][j,i] + 0.5
    return adj

#####################################################
#                 Main                              #
#####################################################
def main():
    f = open("sqfield-rankability.csv","w+")
    f.write('Year, Round, specR \n')
    years = [2013,2014,2015,2016,2017,2018]
    for k in range(len(years)):
        adj = read_data(years[k])
        f.write(str('%d' % years[k])+',,'+'\n')
        for r in range(len(adj)):
            a = adj[r]
            if(k<=1):
                # double round-robin
                f.write(','+str('%d' % (r+1))+str(',%.4f' % spec2R(a))+'\n')
            else:
                # single round-robin
                f.write(','+str('%d' % (r+1))+str(',%.4f' % specR(a))+'\n')    
        
main()